from app.schemas.knowledge import KnowledgeBaseEntry
from app.services.llm_service import LLMService
from app.services.response_policy import ResponsePolicy

class ExplanationAgent:
    """
    Uses the LLM to explain institute methodology based strictly on Knowledge Base JSON.
    """
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def explain(self, query: str, kb_entry: KnowledgeBaseEntry) -> tuple[str, dict]:
        prompt = f"""
        You are an expert MBA Admissions Assistant.
        A user has asked: "{query}"

        You must answer their question using ONLY the following verified data for {kb_entry.institute}.
        Please do not invent any formulas, minimum cutoffs, or weightages. If the data provided below says 'Lack of verified published data', tell the user explicitly that it is not published.
        Avoid revealing internal benchmark values such as call threshold composite, typical composite, strong composite, CAT benchmarks, or internal gaps.

        Institute: {kb_entry.institute}
        Methodology: {kb_entry.shortlisting_methodology}
        Key Factors: {', '.join(kb_entry.key_factors)}
        Formula: {kb_entry.formula_summary}
        Important Exceptions: {', '.join(kb_entry.important_exceptions)}
        Confidence Level: {kb_entry.confidence}
        
        Provide a concise, direct, and conversational text answer.
        """

        raw_response = self.llm_service.generate_text(prompt)
        final_response = ResponsePolicy.apply_guardrails(raw_response, kb_entry.confidence)
        
        visual_payload = {
            "type": "formula",
            "data": {
                "institute": kb_entry.institute,
                "formula": kb_entry.formula_summary,
                "key_factors": kb_entry.key_factors
            }
        }
        
        return final_response, visual_payload
