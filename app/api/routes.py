from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError

from app.services import (
    LLMService, 
    ExplanationAgent, 
    SemanticParser, 
    ProfileExtractionAgent,
    SessionManager,
    ProfileValidator,
    ClarifyingQuestionGenerator,
    ProfileScoringEngine,
    CompetitivenessClassifier,
    ResponsePlanGenerator,
    EvaluationAgent,
    PercentileEstimatorService,
    TargetPercentileAgent,
    TelemetryService,
    GuardrailVerifier
)
from app.repositories import (
    InstituteRepository, 
    KnowledgeBaseRepository,
    ScoringRuleRepository,
    BenchmarkRepository
)
from app.services.recommendation_engine import RecommendationEngine
from app.services.recommendation_agent import RecommendationAgent

router = APIRouter()

# Initialize Repositories
institute_repo = InstituteRepository()
kb_repo = KnowledgeBaseRepository()
scoring_repo = ScoringRuleRepository()
benchmark_repo = BenchmarkRepository()

# Initialize Services
llm_service = LLMService()
session_manager = SessionManager()
telemetry = TelemetryService()
guardrail_verifier = GuardrailVerifier(llm_service=llm_service)
agent = ExplanationAgent(llm_service)

from app.services.audio_service import TextToSpeechService
from fastapi.responses import FileResponse
import tempfile
import edge_tts
import asyncio
import os

# Get all valid IDs dynamically for the parser prompt
valid_institute_ids = [inst.institute_id for inst in institute_repo.get_all()]
valid_institute_ids.append("blacki")
parser = SemanticParser(llm_service, valid_institute_ids)
profile_extractor = ProfileExtractionAgent(llm_service)
question_generator = ClarifyingQuestionGenerator(llm_service)

# Stage 3 Singletons
benchmark_repo = BenchmarkRepository()
scoring_engine = ProfileScoringEngine()
competitiveness_classifier = CompetitivenessClassifier(benchmark_repo)
response_plan_generator = ResponsePlanGenerator()
evaluation_agent = EvaluationAgent(llm_service)

# Stage 4 Singletons
percentile_estimator = PercentileEstimatorService(benchmark_repo)
target_percentile_agent = TargetPercentileAgent(llm_service)

# Stage 5 Singletons
recommendation_engine = RecommendationEngine(scoring_engine, benchmark_repo)
recommendation_agent = RecommendationAgent(llm_service)

class AskRequest(BaseModel):
    query: str
    session_id: str = "default_session"

class AskResponse(BaseModel):
    intent: str
    institute_id: str | None = None
    answer: str
    profile_complete: bool = False
    visual_payload: dict | None = None

def _process_ask(query: str, session_id: str) -> AskResponse:
    # 1. Unified Semantic Parsing
    parsed = parser.parse(query)
    intent = parsed.intent
    
    # Log Analytics
    telemetry.track_event("intent.classified", session_id, {"intent": intent, "institute": parsed.institute_ids})
    
    # Check if the parser found new institutes, otherwise fallback to session memory
    profile = session_manager.get_profile(session_id)
    institute_ids = parsed.institute_ids
    if not institute_ids and profile.target_institute:
        institute_ids = [profile.target_institute]
        
    # Save it back to memory if valid
    if institute_ids:
        profile.target_institute = institute_ids[0]
        
    # intercept blacki
    expanded_institutes = []
    for inst in institute_ids:
        if inst == "blacki":
            expanded_institutes.extend(["iim_ahmedabad", "iim_bangalore", "iim_calcutta", "iim_lucknow", "iim_kozhikode", "iim_indore"])
        else:
            expanded_institutes.append(inst)
            
    # deduplicate
    expanded_institutes = list(dict.fromkeys(expanded_institutes))
        
    # Heuristic Context Restoration:
    if intent in ["UNKNOWN", "PROFILE_EVALUATION"] and profile.last_intent:
        intent = profile.last_intent
    if intent == "TARGET_PERCENTILE" and profile.last_intent == "COLLEGE_RECOMMENDATION" and not parsed.institute_ids:
        intent = profile.last_intent
        
    profile.last_intent = intent
        
    if intent == "OUT_OF_DOMAIN":
        telemetry.track_event("guardrail.blocked", session_id, {"reason": "OUT_OF_DOMAIN"})
        return AskResponse(
            intent=intent,
            answer="I can't help with that in this voice bot. This assistant is focused only on MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. You can ask me something like: 'What percentile should I target for IIM Bangalore?' or 'Is my profile good for FMS?'",
            profile_complete=False
        )
        
    if intent == "OUT_OF_DOMAIN_CLYMBER":
        telemetry.track_event("guardrail.blocked", session_id, {"reason": "OUT_OF_DOMAIN_CLYMBER"})
        return AskResponse(
            intent=intent,
            answer="This voice bot is currently limited to MBA admissions guidance, profile evaluation, target percentile planning, college recommendations, and institute shortlisting methodology. For CAT preparation, DILR, QA, VARC, mocks, mentorship, scholarships, or course-related information, please check clymber.ai. I can still help you understand what percentile you should target or which colleges fit your profile.",
            profile_complete=False
        )
    
    if intent == "PROFILE_EVALUATION" or intent == "UNKNOWN":
        # Stage 2: Profile Intake Flow (We fallback to this if UNKNOWN just in case they are just giving profile)
        
        # Extract Delta
        try:
            delta = profile_extractor.extract(query)
            # Merge into Memory
            profile = session_manager.update_profile(session_id, delta)
        except ValidationError as e:
            return AskResponse(
                intent="PROFILE_EVALUATION",
                answer="It looks like one of the numbers you provided is out of valid bounds (for example, percentiles must be 100 or below). Could you check and provide it again?",
                profile_complete=False
            )
        
        # Validate (Evaluating a profile requires the exam score to give an accurate deterministic result)
        missing_fields = ProfileValidator.get_missing_fields(profile, require_exam_score=True)
        
        if missing_fields:
            # Generate Premium Clarifying Question
            provided_fields = profile.model_dump(exclude_none=True)
            question = question_generator.generate(missing_fields, provided_fields, query)
            return AskResponse(
                intent="PROFILE_EVALUATION",
                institute_id=expanded_institutes[0] if expanded_institutes else None,
                answer=question,
                profile_complete=False
            )
        else:
            # Profile is Complete. Check if they asked for a specific institute.
            if expanded_institutes:
                # Stage 3 Flow: Score Profile
                from app.schemas.scoring import EvaluationMode
                mode = EvaluationMode.SCORE_KNOWN if profile.actual_percentile is not None else EvaluationMode.PRE_CAT
                
                plans = []
                for inst in expanded_institutes:
                    score_result = scoring_engine.calculate_score(profile, inst)
                    evaluation = competitiveness_classifier.classify(score_result, profile.category, mode)
                    plans.append(response_plan_generator.generate_plan(evaluation))
                
                plan_text = "\n\n".join(plans)
                
                # Use Evaluation Agent to verbalize the plan
                answer = evaluation_agent.explain(query, plan_text)
                
                return AskResponse(
                    intent="PROFILE_EVALUATION",
                    institute_id=expanded_institutes[0],
                    answer=answer,
                    profile_complete=True,
                    visual_payload={
                        "type": "evaluation", 
                        "data": {
                            "label": evaluation.user_facing_label,
                            "composite_score": evaluation.composite_score,
                            "strengths": evaluation.strengths,
                            "risks": evaluation.risks
                        }
                    }
                )
            else:
                return AskResponse(
                    intent="PROFILE_EVALUATION",
                    answer="Excellent! Your profile is complete. Which institute would you like me to evaluate your chances for?",
                    profile_complete=True
                )
            
    if intent == "COLLEGE_RECOMMENDATION":
        # Extract Delta
        try:
            delta = profile_extractor.extract(query)
            profile = session_manager.update_profile(session_id, delta)
        except ValidationError as e:
            return AskResponse(
                intent="COLLEGE_RECOMMENDATION",
                answer="It looks like one of the numbers you provided is out of valid bounds (for example, percentiles must be 100 or below). Could you check and provide it again?",
                profile_complete=False
            )
        
        # We need the full profile (including exam score if they want realistic recommendations)
        if profile.actual_percentile is None:
            return AskResponse(
                intent="COLLEGE_RECOMMENDATION",
                institute_id=expanded_institutes[0] if expanded_institutes else None,
                answer="I can't create a reliable college recommendation list without some CAT estimate, because the same profile can lead to very different college options at different percentiles. You can share your expected percentile, current mock percentile, or even a rough target range, and I'll use that to build the recommendation buckets.",
                profile_complete=False
            )
            
        missing_fields = ProfileValidator.get_missing_fields(profile, require_exam_score=True)
        if missing_fields:
            provided_fields = profile.model_dump(exclude_none=True)
            question = question_generator.generate(missing_fields, provided_fields, query)
            return AskResponse(
                intent="COLLEGE_RECOMMENDATION",
                institute_id=expanded_institutes[0] if expanded_institutes else None,
                answer=question,
                profile_complete=False
            )
            
        # Profile complete, generate report
        report = recommendation_engine.generate_recommendations(profile)
        answer, payload = recommendation_agent.generate_response(report)
        
        return AskResponse(
            intent="COLLEGE_RECOMMENDATION",
            institute_id=expanded_institutes[0] if expanded_institutes else None,
            answer=answer,
            profile_complete=True,
            visual_payload=payload
        )
        
    if intent == "TARGET_PERCENTILE":
        # Extract Delta to be safe
        try:
            delta = profile_extractor.extract(query)
            profile = session_manager.update_profile(session_id, delta)
        except ValidationError as e:
            return AskResponse(
                intent="TARGET_PERCENTILE",
                answer="It looks like one of the numbers you provided is out of valid bounds (for example, percentiles must be 100 or below). Could you check and provide it again?",
                profile_complete=False
            )
        
        # Ensure we have the minimum profile fields required for target math (Academics + Work Ex)
        missing_fields = ProfileValidator.get_missing_fields(profile)
        # We don't necessarily need 'actual_percentile' to calculate the required percentile
        # But we do need the others. Let's just check standard profile completeness.
        if missing_fields:
            provided_fields = profile.model_dump(exclude_none=True)
            question = question_generator.generate(missing_fields, provided_fields, query)
            return AskResponse(
                intent="TARGET_PERCENTILE",
                answer=question,
                profile_complete=False
            )
            
        if not expanded_institutes:
            return AskResponse(
                intent="TARGET_PERCENTILE",
                answer="Which institute would you like me to calculate the target percentile for?",
                profile_complete=True
            )
            
        answers = []
        payloads = []
        for inst in expanded_institutes:
            target_result = percentile_estimator.estimate_target(profile, inst)
            answer, payload = target_percentile_agent.generate_response(target_result, profile.model_dump(exclude_none=True))
            answers.append(answer)
            if payload: payloads.append(payload)
            
        final_answer = "\n\n".join(answers)
        
        return AskResponse(
            intent="TARGET_PERCENTILE",
            institute_id=expanded_institutes[0],
            answer=final_answer,
            profile_complete=True,
            visual_payload=payloads[0] if payloads else None
        )

    if intent != "METHODOLOGY":
        return AskResponse(
            intent=intent,
            answer="I am an admissions assistant. Right now, I can only help you understand how specific institutes shortlist candidates, evaluate your profile, or estimate your target percentile.",
            profile_complete=False
        )
        
    # 2. Check Institute Validity
    if not expanded_institutes:
        return AskResponse(
            intent=intent,
            answer="I couldn't identify the institute you are asking about. Could you please specify the name clearly (e.g., 'IIM Ahmedabad')?",
            profile_complete=False
        )
        
    # 3. Methodolgy Flow (Stage 1)
    answers = []
    payloads = []
    for inst in expanded_institutes:
        kb_entry = kb_repo.get_knowledge(inst)
        if not kb_entry:
            answers.append(f"I'm sorry, but I don't have verified methodology data for {inst} in my database.")
            continue
            
        try:
            answer, payload = agent.explain(query, kb_entry)
            answers.append(answer)
            if payload: payloads.append(payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
    final_answer = "\n\n".join(answers)
    return AskResponse(
        intent=intent,
        institute_id=expanded_institutes[0],
        answer=final_answer,
        profile_complete=False,
        visual_payload=payloads[0] if payloads else None
    )

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    query = request.query
    session_id = request.session_id
    
    # 1. Process the request to get a draft response
    try:
        response = _process_ask(query, session_id)
    except Exception as e:
        telemetry.track_event("engine.error", session_id, {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))
        
    # 2. Safety & Scope Guardrails
    verification = guardrail_verifier.verify_final_answer(response.answer)
    
    final_answer = response.answer
    if verification.status == "BLOCKED":
        telemetry.track_event("guardrail.blocked", session_id, {
            "failed_checks": verification.failed_checks,
            "draft_answer": response.answer
        })
        final_answer = guardrail_verifier.get_fallback_answer()
        response.answer = final_answer
        
    # 3. Log Audit Trace
    profile = session_manager.get_profile(session_id)
    telemetry.log_audit_trace(
        session_id=session_id,
        turn_id=query[:10], # simplistic turn id
        user_query=query,
        intent=response.intent,
        extracted_profile=profile.model_dump(),
        response_plan={"draft_answer": response.answer},
        final_answer=final_answer,
        guardrail_passed=(verification.status == "APPROVED")
    )
    
    return response

@router.delete("/session/{session_id}")
def clear_session(session_id: str):
    session_manager.clear_session(session_id)
    return {"status": "success", "message": f"Session {session_id} memory cleared."}

@router.post("/tts")
async def generate_tts(request: AskRequest):
    """Generates TTS audio file for the frontend."""
    text = request.query
    import re
    clean_text = re.sub(r'[*_]{1,3}', '', text)
    clean_text = re.sub(r'#+\s*', '', clean_text)
    clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)
    
    # Create temp file
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    
    communicate = edge_tts.Communicate(clean_text, "en-IN-NeerjaExpressiveNeural")
    await communicate.save(path)
    
    return FileResponse(path, media_type="audio/mpeg", background=None)
