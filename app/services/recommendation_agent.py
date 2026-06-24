from app.services.llm_service import LLMService
from app.schemas.profile import RecommendationReport

class RecommendationAgent:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_response(self, report: RecommendationReport) -> tuple[str, dict]:
        """
        Generates a concise voice response explaining the bucketed recommendations and biggest gaps.
        """
        
        # Convert the complex report into a simplified string for the LLM prompt
        strong_str = ", ".join([r.institute_id for r in report.strong_colleges]) or "None"
        realistic_str = ", ".join([r.institute_id for r in report.realistic_colleges]) or "None"
        stretch_str = ", ".join([r.institute_id for r in report.stretch_colleges]) or "None"
        ambitious_str = ", ".join([r.institute_id for r in report.ambitious_colleges]) or "None"
        
        fixed_gap = "None"
        if report.gap_report and report.gap_report.biggest_fixed_bottleneck:
            bg = report.gap_report.biggest_fixed_bottleneck
            fixed_gap = f"{bg.factor_name} ({bg.description})"
            
        controllable_gap = "None"
        if report.gap_report and report.gap_report.biggest_controllable_lever:
            bg = report.gap_report.biggest_controllable_lever
            controllable_gap = f"{bg.factor_name} ({bg.description})"

        prompt = f"""
        You are an elite MBA Admissions Assistant providing a voice-first College Recommendation.
        The user asked which colleges are realistic for them.
        Our deterministic recommendation engine has evaluated their profile across all tracked B-Schools and generated these buckets:
        
        Strong Chances: {strong_str}
        Realistic: {realistic_str}
        Stretch: {stretch_str}
        Ambitious: {ambitious_str}
        
        Gap Analysis (Based on their top realistic/stretch college):
        Biggest Fixed Bottleneck (they cannot change this): {fixed_gap}
        Biggest Controllable Lever (they must focus on this): {controllable_gap}
        
        Instructions:
        1. Give a conversational, concise summary. 
        2. Please avoid reading every single list. Highlight the top 1-2 realistic options and top 1 stretch option.
        3. Explain their biggest fixed bottleneck gently.
        4. Emphasize their biggest controllable lever (usually CAT) as their main focus.
        5. Please avoid hallucinating any rankings, guaranteed calls, or institutes not mentioned above.
        6. Keep it short and natural for a voice response (under 4 sentences if possible).
        """

        response_text = self.llm_service.generate_text(prompt)
        
        visual_payload = {
            "type": "college_recommendations",
            "data": {
                "strong": [r.institute_id for r in report.strong_colleges],
                "realistic": [r.institute_id for r in report.realistic_colleges],
                "stretch": [r.institute_id for r in report.stretch_colleges],
                "ambitious": [r.institute_id for r in report.ambitious_colleges],
                "bottleneck": fixed_gap,
                "lever": controllable_gap
            }
        }
        
        return response_text, visual_payload
