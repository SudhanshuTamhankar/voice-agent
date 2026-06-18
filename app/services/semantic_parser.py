import json
from typing import Optional
from pydantic import BaseModel, ValidationError
from app.services.llm_service import LLMService

class ParserOutput(BaseModel):
    intent: str
    institute_id: Optional[str] = None

class SemanticParser:
    """
    Uses the LLM to parse a natural language query into a structured JSON object
    containing the user's intent and the extracted institute_id.
    """
    def __init__(self, llm_service: LLMService, valid_institutes: list[str]):
        self.llm_service = llm_service
        self.valid_institutes = valid_institutes

    def parse(self, query: str) -> ParserOutput:
        institutes_str = ", ".join(self.valid_institutes)
        prompt = f"""
        You are a Semantic Parser for an MBA Admissions Assistant.
        Read the user's query and extract their intent and the target institute.
        
        Valid Intent Values:
        - METHODOLOGY (Asking about how an institute shortlists, factors used, academic weight, etc.)
        - PROFILE_EVALUATION (Asking to evaluate their profile, asking if their profile is good for an institute, or providing profile details like 10th, 12th, CAT, work experience)
        - TARGET_PERCENTILE (Asking about cut-offs, required scores, or target percentiles for an institute)
        - COLLEGE_RECOMMENDATION (Asking which colleges are realistic, which institutes they can get into, etc.)
        - UNKNOWN (For anything else)
        
        Valid Institute IDs (If the user mentions an institute, map it to one of these IDs. If they mention an institute NOT in this list, or no institute at all, return null):
        [{institutes_str}]

        User Query: "{query}"
        
        Return ONLY a JSON object matching this schema:
        {{
            "intent": "string",
            "institute_id": "string or null"
        }}
        """

        raw_json_str = self.llm_service.generate_json(prompt)
        try:
            data = json.loads(raw_json_str)
            return ParserOutput(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            # Fallback if the LLM fails to format correctly
            return ParserOutput(intent="UNKNOWN", institute_id=None)
