from typing import Optional
from pydantic import BaseModel, ValidationError
import json
from app.services.llm_service import LLMService

class VerificationResult(BaseModel):
    status: str  # "APPROVED" or "BLOCKED"
    failed_checks: list[str] = []
    reason: str = ""

class GuardrailVerifier:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def verify_final_answer(self, draft_answer: str) -> VerificationResult:
        """
        Uses an LLM judge to enforce safety and scope guardrails on the final text 
        before it is sent to TTS or the user.
        """
        prompt = f"""
        You are the Quality Reviewer for an MBA Admissions Assistant.
        Your job is to read the proposed draft answer and ensure it follows these guidelines:

        Guidelines:
        1. No Guarantees: The assistant should avoid guaranteeing a call or admission.
        2. Be Polite: The assistant should be encouraging. Explaining mathematical unlikelihoods or limits is fine.
        3. Scope Check: The assistant should focus on admissions, target percentiles, profiles, and methodologies. Do not offer tutoring, resume writing, SOP writing, or interview prep.
        4. Relevance: Please filter out open-web trivia or general knowledge questions.

        Draft Answer to evaluate:
        "{draft_answer}"

        Determine if the draft answer violates ANY of the guidelines above.
        Return ONLY a JSON object matching this schema:
        {{
            "status": "APPROVED" or "BLOCKED",
            "failed_checks": ["List of violated rules if any", ...],
            "reason": "Short explanation"
        }}
        """
        try:
            raw_json = self.llm_service.generate_json(prompt)
            data = json.loads(raw_json)
            result = VerificationResult(**data)
            return result
        except (json.JSONDecodeError, ValidationError) as e:
            # Fail closed for safety
            return VerificationResult(
                status="BLOCKED",
                failed_checks=["JSON Parsing Error in Verifier"],
                reason=str(e)
            )

    def get_fallback_answer(self) -> str:
        return "I'm sorry, I cannot provide a definitive or guaranteed prediction about that. I can only provide mathematical estimates based on historical composite formulas. Let's focus on your target percentile or evaluating your current profile strength."
