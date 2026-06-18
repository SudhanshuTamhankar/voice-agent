import json
from pydantic import ValidationError
from app.services.llm_service import LLMService
from app.schemas.profile import ProfileDelta

class ProfileExtractionAgent:
    """
    Extracts profile fields from messy natural language into a strict ProfileDelta schema.
    """
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def extract(self, query: str) -> ProfileDelta:
        prompt = f"""
        You are a Profile Extraction Agent for an MBA Admissions Assistant.
        Read the user's message and extract any mentioned profile fields.

        Valid Categories: General, EWS, OBC, SC, ST, PwD
        Valid Genders: Male, Female, Transgender
        Valid Streams: Engineering, Commerce, Arts, Science, etc.
        Scores: Extract numerical values for 10th, 12th, and graduation.
        Work Experience: Extract or convert to months (e.g. '2 years' = 24). If they say 'fresher', work_ex_months = 0.
        Percentile: If the user mentions any CAT score or percentile (e.g. '99.67 percentile', 'my cat is 99'), extract the numerical value and assign it to the 'actual_percentile' field. DO NOT leave it null if a number is provided.

        User Message: "{query}"
        
        Return ONLY a JSON object matching this exact schema:
        {{
            "category": "string or null",
            "gender": "string or null",
            "class_10_score": float or null,
            "class_12_score": float or null,
            "graduation_score": float or null,
            "graduation_stream": "string or null",
            "work_ex_months": integer or null,
            "target_exam": "string or null",
            "actual_percentile": float or null
        }}
        """

        raw_json_str = self.llm_service.generate_json(prompt)
        try:
            data = json.loads(raw_json_str)
            return ProfileDelta(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            return ProfileDelta()
