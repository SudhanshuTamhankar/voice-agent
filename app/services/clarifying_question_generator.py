from typing import List
from app.services.llm_service import LLMService

class ClarifyingQuestionGenerator:
    """
    Uses the LLM to generate a premium conversational follow-up question
    asking the user for their missing profile fields.
    """
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate(self, missing_fields: List[str], provided_fields: dict) -> str:
        # Convert internal field names to readable strings
        readable_fields = [f.replace("_", " ").title() for f in missing_fields]
        missing_str = ", ".join(readable_fields)
        
        provided_str = ", ".join([f"{k.replace('_', ' ').title()}: {v}" for k,v in provided_fields.items() if v is not None])

        prompt = f"""
        You are an elite MBA Admissions Assistant.
        You are in the middle of taking down a user's academic and background profile to evaluate their chances at top IIMs.
        
        The user has provided these fields so far: {provided_str if provided_str else "None"}
        
        HOWEVER, you still urgently need the following missing fields to run a deterministic calculation:
        [{missing_str}]
        
        Write a single, conversational, encouraging sentence acknowledging what they just gave you (if any), 
        and specifically asking them to provide the missing fields.
        Do NOT answer any admissions questions or output JSON. Output just the conversational text.
        """

        return self.llm_service.generate_text(prompt)
