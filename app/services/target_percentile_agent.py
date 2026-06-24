from app.services.llm_service import LLMService
from app.services.percentile_estimator_service import PercentileTargetResult

class TargetPercentileAgent:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_response(self, target_result: PercentileTargetResult, user_profile: dict) -> tuple[str, dict]:
        """
        Generates a human-readable response based on the deterministic Target Percentile math.
        """
        if target_result.is_possible and target_result.percentile_range is not None:
            # We have a specific percentile to target
            prompt = f"""
            You are an MBA Admissions Assistant.
            
            The user wants to know what CAT percentile they should target for {target_result.institute_id}.
            Our deterministic math engine has calculated the exact required percentile range based on their profile.
            
            Target Institute: {target_result.institute_id}
            User Profile: {user_profile}
            Math Engine Required Range: {target_result.percentile_range} percentile
            Engine Explanation: {target_result.explanation}
            
            Instructions:
            1. Formulate a response using EXACTLY this conversational structure:
               "For {target_result.institute_id}, your target should be around {target_result.percentile_range} percentile. This is reverse-engineered from the institute's composite-score logic for your profile and category. Treat it as a planning range, not a cutoff or guarantee. Since CAT is still controllable, aim for the maximum possible score."
            2. State that this is an estimation based on historical benchmarks and their current profile gap.
            3. DO NOT hallucinate any math or change the numbers.
            4. Emphasize that they should aim for the maximum possible score rather than just the lower end of this range.
            5. NEVER say "guaranteed call", "safe", or "cutoff".
            """
        elif target_result.is_possible:
            # Possible, but opaque or generic exam (like XLRI)
            prompt = f"""
            You are an MBA Admissions Assistant.
            
            The user wants to know what percentile they should target for {target_result.institute_id}.
            
            Target Institute: {target_result.institute_id}
            User Profile: {user_profile}
            Engine Explanation: {target_result.explanation}
            
            Instructions:
            1. Explain to the user that {target_result.institute_id} relies primarily on the exam score directly (or an opaque holistic process), rather than a mathematical composite score combining academics and work experience.
            2. Advise them to aim for the historical high percentile range for that institute/exam.
            3. DO NOT invent a specific percentile number if none is provided.
            """
        else:
            # Mathematically impossible or no data
            prompt = f"""
            You are an MBA Admissions Assistant.
            
            The user wants to know what CAT percentile they should target for {target_result.institute_id}.
            
            Target Institute: {target_result.institute_id}
            User Profile: {user_profile}
            Engine Explanation: {target_result.explanation}
            
            Instructions:
            1. If the Engine Explanation mentions that there is "No benchmark data" or "No target composite score", tell the user that we currently lack the historical cut-off data needed to calculate a target percentile for {target_result.institute_id}.
            2. If the Engine Explanation mentions that it is "mathematically impossible" because of their current profile, gently explain the hard truth: based on their fixed academic profile, they cannot reach the safe composite score even with a 100 percentile. Be empathetic but factual. Suggest FMS Delhi or XLRI instead.
            3. DO NOT hallucinate that an institute rejected them for academics if the Engine Explanation says there is no benchmark data!
            """

        response_text = self.llm_service.generate_text(prompt)
        
        visual_payload = {
            "type": "percentile_target",
            "data": {
                "institute_id": target_result.institute_id,
                "is_possible": target_result.is_possible,
                "percentile_range": target_result.percentile_range,
                "explanation": target_result.explanation
            }
        }
        
        return response_text, visual_payload
