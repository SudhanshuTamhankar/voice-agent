from app.schemas.scoring import EvaluationResult, EvaluationMode

class ResponsePlanGenerator:
    def generate_plan(self, evaluation: EvaluationResult) -> str:
        """
        Formats the strict deterministic scoring output into a text plan 
        for the LLM ExplanationAgent to read and verbalize.
        """
        plan = [
            f"=== DETERMINISTIC ADMISSIONS EVALUATION FOR {evaluation.institute_id.upper()} ===",
            f"Mode: {evaluation.mode.value}",
            f"Competitiveness Label: {evaluation.user_facing_label}",
            f"Total Composite Score: {evaluation.composite_score}",
            f"Strengths: {evaluation.strengths}",
            f"Risks: {evaluation.risks}",
            f"Next Action: {evaluation.next_action}",
            "Score Breakdown:"
        ]
        
        for factor in evaluation.factors:
            plan.append(f"- {factor.factor_name}: {factor.score_awarded} pts")
        
        plan.append("")

        plan.append("=== INSTRUCTIONS FOR LLM EXPLANATION ===")
        plan.append("1. Do NOT invent or calculate any new numbers or raw benchmarks.")
        plan.append("2. Explain the Competitiveness Label to the user clearly.")
        plan.append("3. Highlight which factors helped them the most and which hurt them.")
        plan.append("4. Follow the strict output contract format for your answer.")
        
        if evaluation.mode == EvaluationMode.PRE_CAT:
            plan.append("5. MANDATORY PRE-CAT RULE: Since CAT is still ahead, do not aim only to clear the estimated range. Push for the maximum possible score because every extra mark improves your options across institutes.")
        else:
            plan.append("5. MANDATORY SCORE-KNOWN RULE: Use current-position wording (e.g. 'With your current score/profile, this appears...'). Avoid effort-based wording such as 'high-effort target' because the score may already be fixed.")

        return "\n".join(plan)
