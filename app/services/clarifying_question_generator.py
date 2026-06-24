from typing import List
from app.services.llm_service import LLMService

class ClarifyingQuestionGenerator:
    """
    Uses the LLM to generate a premium conversational follow-up question
    asking the user for their missing profile fields.
    """
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate(self, missing_fields: List[str], provided_fields: dict, user_query: str = "") -> str:
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
        
        The user's latest message was: "{user_query}"
        
        Instructions:
        1. If the user's latest message is asking a meta-question about the profile you captured (e.g., "what is my 10th percentage you captured?", "did you get my work ex?"), ANSWER their question first using the provided fields data.
        2. Then, write a single, conversational, encouraging sentence acknowledging what they just gave you (if any), and specifically ask them to provide the missing fields.
        3. Do NOT answer any specific admissions evaluation questions (e.g., "am I good enough?") because you don't have the math results yet.
        4. Output just the conversational text.
        """

        return self.llm_service.generate_text(prompt)
