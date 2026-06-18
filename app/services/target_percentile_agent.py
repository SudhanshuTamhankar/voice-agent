from app.services.llm_service import LLMService
from app.services.percentile_estimator_service import PercentileTargetResult

class TargetPercentileAgent:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def generate_response(self, target_result: PercentileTargetResult, user_profile: dict) -> str:
        """
        Generates a human-readable response based on the deterministic Target Percentile math.
        """
        if target_result.is_possible and target_result.required_percentile is not None:
            # We have a specific percentile to target
            prompt = f"""
            You are an MBA Admissions Assistant.
            
            The user wants to know what CAT percentile they should target for {target_result.institute_id}.
            Our deterministic math engine has calculated the exact required percentile based on their profile.
            
            Target Institute: {target_result.institute_id}
            User Profile: {user_profile}
            Math Engine Required Percentile: {target_result.required_percentile}%
            Engine Explanation: {target_result.explanation}
            
            Instructions:
            1. Formulate a response explaining that based on their academic profile and work experience, they need a CAT percentile of approximately {target_result.required_percentile}% to hit the safe composite score.
            2. State that this is an estimation based on historical benchmarks and their current profile gap.
            3. DO NOT hallucinate any math. DO NOT recalculate the percentile.
            4. Emphasize that the required percentile might shift depending on the difficulty of the CAT paper and the pool of applicants in the actual year, so they should treat it as a target range rather than a guaranteed cut-off.
            5. NEVER say "guaranteed call". Use words like "safe benchmark", "competitive range", or "target percentile".
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
        return response_text
