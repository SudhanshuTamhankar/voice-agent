import json
from typing import Optional
from pydantic import BaseModel, ValidationError
from app.services.llm_service import LLMService

class ParserOutput(BaseModel):
    intent: str
    institute_ids: list[str] = []

class SemanticParser:
    """
    Uses the LLM to parse a natural language query into a structured JSON object
    containing the user's intent and the extracted institute_ids.
    """
    def __init__(self, llm_service: LLMService, valid_institutes: list[str]):
        self.llm_service = llm_service
        self.valid_institutes = valid_institutes

    def parse(self, query: str) -> ParserOutput:
        institutes_str = ", ".join(self.valid_institutes)
        prompt = f"""
        You are a Semantic Parser for an MBA Admissions Assistant.
        Read the user's query and extract their intent and all target institutes mentioned.
        
        Valid Intent Values:
        - METHODOLOGY (Asking about how an institute shortlists, factors used, academic weight, etc.)
        - PROFILE_EVALUATION (Asking to evaluate their profile, asking if their profile is good for an institute, providing profile details like 10th/12th/CAT/workex, OR asking for their composite score, actual score, or score breakdown)
        - TARGET_PERCENTILE (Asking about cut-offs, required CAT percentiles to get in, or target scores to aim for on the CAT exam)
        - COLLEGE_RECOMMENDATION (Asking which colleges are realistic, which institutes they can get into, etc.)
        - OUT_OF_DOMAIN (For fully unrelated queries like general trivia, chit-chat, weather, capital of India, NEET, JEE)
        - OUT_OF_DOMAIN_CLYMBER (For CAT-prep related but unsupported queries like DILR/QA/VARC study plans, mock tests, mentorship, courses, pricing, or scholarships)
        - UNKNOWN (For MBA-related queries that don't fit the above)
        
        Valid Institute IDs (If the user mentions an institute, map it to one of these IDs. If they mention multiple institutes, return a list of all matching IDs. If no institute is mentioned, return an empty list):
        [{institutes_str}]
        
        IMPORTANT: If the user says "BLACKI" or "blacki", extract the literal string "blacki" and add it to the list.

        User Query: "{query}"
        
        Return ONLY a JSON object matching this schema:
        {{
            "intent": "string",
            "institute_ids": ["string", "string"]
        }}
        """

        raw_json_str = self.llm_service.generate_json(prompt)
        try:
            data = json.loads(raw_json_str)
            return ParserOutput(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            # Fallback if the LLM fails to format correctly
            return ParserOutput(intent="UNKNOWN", institute_ids=[])
