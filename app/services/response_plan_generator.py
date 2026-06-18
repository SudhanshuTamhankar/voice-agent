from app.schemas.scoring import EvaluationResult

class ResponsePlanGenerator:
    def generate_plan(self, evaluation: EvaluationResult) -> str:
        """
        Formats the strict deterministic scoring output into a text plan 
        for the LLM ExplanationAgent to read and verbalize.
        """
        plan = [
            f"=== DETERMINISTIC ADMISSIONS EVALUATION FOR {evaluation.institute_id.upper()} ===",
            f"Total Composite Score: {evaluation.composite_score}",
            f"Competitiveness Label: {evaluation.label.value}",
            ""
        ]

        if evaluation.safe_benchmark is not None:
            plan.append(f"Safe Benchmark (Strong Composite): {evaluation.safe_benchmark}")
            plan.append(f"Stretch Benchmark (Call Threshold): {evaluation.stretch_benchmark}")
            plan.append("")

        plan.append("--- FACTOR BREAKDOWN ---")
        for factor in evaluation.factors:
            plan.append(f"Factor: {factor.factor_name}")
            plan.append(f"Score Awarded: {factor.score_awarded} (Max: {factor.max_possible_score or 'Unknown'})")
            plan.append(f"Reasoning: {factor.explanation}")
            plan.append(f"Rule Cited: {factor.rule_cited}")
            plan.append("")

        plan.append("=== INSTRUCTIONS FOR LLM EXPLANATION ===")
        plan.append("1. Do NOT invent or calculate any new numbers. Rely EXACTLY on the numbers provided above.")
        plan.append("2. Explain the Competitiveness Label to the user clearly.")
        plan.append("3. Highlight which factors helped them the most and which hurt them.")
        plan.append("4. Keep it conversational and voice-friendly.")

        return "\n".join(plan)
