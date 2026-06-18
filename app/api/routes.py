from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
    TargetPercentileAgent
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

# Initialize Singletons
institute_repo = InstituteRepository()
kb_repo = KnowledgeBaseRepository()

llm_service = LLMService()
agent = ExplanationAgent(llm_service)
session_manager = SessionManager()

# Get all valid IDs dynamically for the parser prompt
valid_institute_ids = [inst.institute_id for inst in institute_repo.get_all()]
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

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    query = request.query
    session_id = request.session_id
    
    # 1. Unified Semantic Parsing
    parsed = parser.parse(query)
    intent = parsed.intent
    
    # Check if the parser found a new institute, otherwise fallback to session memory
    profile = session_manager.get_profile(session_id)
    institute_id = parsed.institute_id or profile.target_institute
    
    # Save it back to memory if valid
    if parsed.institute_id:
        profile.target_institute = parsed.institute_id
    
    if intent == "PROFILE_EVALUATION" or intent == "UNKNOWN":
        # Stage 2: Profile Intake Flow (We fallback to this if UNKNOWN just in case they are just giving profile)
        
        # Extract Delta
        delta = profile_extractor.extract(query)
        
        # Merge into Memory
        profile = session_manager.update_profile(session_id, delta)
        
        # Validate (Evaluating a profile requires the exam score to give an accurate deterministic result)
        missing_fields = ProfileValidator.get_missing_fields(profile, require_exam_score=True)
        
        if missing_fields:
            # Generate Premium Clarifying Question
            provided_fields = profile.model_dump(exclude_none=True)
            question = question_generator.generate(missing_fields, provided_fields)
            return AskResponse(
                intent="PROFILE_EVALUATION",
                institute_id=institute_id,
                answer=question,
                profile_complete=False
            )
        else:
            # Profile is Complete. Check if they asked for a specific institute.
            if institute_id:
                # Stage 3 Flow: Score Profile
                score_result = scoring_engine.calculate_score(profile, institute_id)
                evaluation = competitiveness_classifier.classify(score_result, profile.category)
                plan_text = response_plan_generator.generate_plan(evaluation)
                
                # Use Evaluation Agent to verbalize the plan
                answer = evaluation_agent.explain(query, plan_text)
                
                return AskResponse(
                    intent="PROFILE_EVALUATION",
                    institute_id=institute_id,
                    answer=answer,
                    profile_complete=True
                )
            else:
                return AskResponse(
                    intent="PROFILE_EVALUATION",
                    answer="Excellent! Your profile is complete. Which institute would you like me to evaluate your chances for?",
                    profile_complete=True
                )
            
    if intent == "COLLEGE_RECOMMENDATION":
        # Extract Delta
        delta = profile_extractor.extract(query)
        profile = session_manager.update_profile(session_id, delta)
        
        # We need the full profile (including exam score if they want realistic recommendations)
        # Actually, if they want recommendations, they usually have an exam score in mind.
        # If they don't, we should ask them for it.
        missing_fields = ProfileValidator.get_missing_fields(profile, require_exam_score=True)
        if missing_fields:
            provided_fields = profile.model_dump(exclude_none=True)
            question = question_generator.generate(missing_fields, provided_fields)
            return AskResponse(
                intent="COLLEGE_RECOMMENDATION",
                institute_id=institute_id,
                answer=question,
                profile_complete=False
            )
            
        # Profile complete, generate report
        report = recommendation_engine.generate_recommendations(profile)
        answer = recommendation_agent.generate_response(report)
        
        return AskResponse(
            intent="COLLEGE_RECOMMENDATION",
            institute_id=institute_id,
            answer=answer,
            profile_complete=True
        )
        
    if intent == "TARGET_PERCENTILE":
        # Extract Delta to be safe
        delta = profile_extractor.extract(query)
        profile = session_manager.update_profile(session_id, delta)
        
        # Ensure we have the minimum profile fields required for target math (Academics + Work Ex)
        missing_fields = ProfileValidator.get_missing_fields(profile)
        # We don't necessarily need 'actual_percentile' to calculate the required percentile
        # But we do need the others. Let's just check standard profile completeness.
        if missing_fields:
            provided_fields = profile.model_dump(exclude_none=True)
            question = question_generator.generate(missing_fields, provided_fields)
            return AskResponse(
                intent="TARGET_PERCENTILE",
                answer=question,
                profile_complete=False
            )
            
        if not institute_id:
            return AskResponse(
                intent="TARGET_PERCENTILE",
                answer="Which institute would you like me to calculate the target percentile for?",
                profile_complete=True
            )
            
        target_result = percentile_estimator.estimate_target(profile, institute_id)
        answer = target_percentile_agent.generate_response(target_result, profile.model_dump(exclude_none=True))
        
        return AskResponse(
            intent="TARGET_PERCENTILE",
            institute_id=institute_id,
            answer=answer,
            profile_complete=True
        )

    if intent != "METHODOLOGY":
        return AskResponse(
            intent=intent,
            answer="I am an admissions assistant. Right now, I can only help you understand how specific institutes shortlist candidates, evaluate your profile, or estimate your target percentile.",
            profile_complete=False
        )
        
    # 2. Check Institute Validity
    if not institute_id:
        return AskResponse(
            intent=intent,
            answer="I couldn't identify the institute you are asking about. Could you please specify the name clearly (e.g., 'IIM Ahmedabad')?",
            profile_complete=False
        )
        
    # 3. Methodolgy Flow (Stage 1)
    kb_entry = kb_repo.get_knowledge(institute_id)
    if not kb_entry:
        return AskResponse(
            intent=intent,
            institute_id=institute_id,
            answer="I'm sorry, but I don't have verified methodology data for that institute in my database.",
            profile_complete=False
        )
        
    # 4. Generate Answer
    try:
        answer = agent.explain(query, kb_entry)
        return AskResponse(
            intent=intent,
            institute_id=institute_id,
            answer=answer,
            profile_complete=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
def clear_session(session_id: str):
    session_manager.clear_session(session_id)
    return {"status": "success", "message": f"Session {session_id} memory cleared."}
