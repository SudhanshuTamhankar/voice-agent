from app.schemas.scoring import CompositeScoreResult, EvaluationResult, CompetitivenessLabel, EvaluationMode
from app.repositories.benchmark_repository import BenchmarkRepository

class CompetitivenessClassifier:
    def __init__(self, benchmark_repository: BenchmarkRepository):
        self.benchmark_repository = benchmark_repository

    def classify(self, score_result: CompositeScoreResult, category: str, mode: EvaluationMode = EvaluationMode.PRE_CAT) -> EvaluationResult:
        benchmark = self.benchmark_repository.get_benchmark(score_result.institute_id, category)
        
        if not benchmark or not benchmark.raw_data:
            return EvaluationResult(
                institute_id=score_result.institute_id,
                composite_score=score_result.total_score,
                mode=mode,
                zone=CompetitivenessLabel.INSUFFICIENT_DATA,
                user_facing_label="Need More Information",
                factors=score_result.factors
            )

        # Extract thresholds
        raw = benchmark.raw_data
        T = raw.get("Call Threshold Composite")
        M = raw.get("Typical Successful Composite")
        H = raw.get("Strong Composite")
        
        zone = CompetitivenessLabel.INSUFFICIENT_DATA
        S = score_result.total_score
        
        if T is not None and M is not None and H is not None:
            if S >= H:
                zone = CompetitivenessLabel.ABOVE_STRONG
            elif S >= M:
                zone = CompetitivenessLabel.TYPICAL_TO_STRONG
            elif S >= T:
                zone = CompetitivenessLabel.CALL_TO_TYPICAL
            elif S >= (T - 2.5):
                zone = CompetitivenessLabel.SLIGHTLY_BELOW_CALL
            else:
                zone = CompetitivenessLabel.OUTSIDE_CURRENT_CALL_RANGE
        elif T is not None and H is not None:
            # Fallback if M is missing
            if S >= H:
                zone = CompetitivenessLabel.ABOVE_STRONG
            elif S >= T:
                zone = CompetitivenessLabel.CALL_TO_TYPICAL
            elif S >= (T - 2.5):
                zone = CompetitivenessLabel.SLIGHTLY_BELOW_CALL
            else:
                zone = CompetitivenessLabel.OUTSIDE_CURRENT_CALL_RANGE

        user_facing_label = self._map_label(zone, mode)

        # Derive simple strengths/risks
        strengths = []
        risks = []
        for factor in score_result.factors:
            if factor.score_awarded > 0:
                strengths.append(f"{factor.factor_name} (awarded {factor.score_awarded})")
            else:
                risks.append(f"{factor.factor_name} (awarded {factor.score_awarded})")

        strengths_str = ", ".join(strengths) if strengths else "None"
        risks_str = ", ".join(risks) if risks else "None"

        if mode == EvaluationMode.PRE_CAT:
            next_action = "Aim for the maximum possible CAT score to maximize optionality."
        else:
            next_action = "Wait for official shortlist or focus on interviews if confident."

        return EvaluationResult(
            institute_id=score_result.institute_id,
            composite_score=score_result.total_score,
            mode=mode,
            zone=zone,
            user_facing_label=user_facing_label,
            strengths=strengths_str,
            risks=risks_str,
            next_action=next_action,
            factors=score_result.factors
        )

    def _map_label(self, zone: CompetitivenessLabel, mode: EvaluationMode) -> str:
        if zone == CompetitivenessLabel.INSUFFICIENT_DATA:
            return "Need More Information"
            
        if mode == EvaluationMode.PRE_CAT:
            mapping = {
                CompetitivenessLabel.ABOVE_STRONG: "Strong Starting Position",
                CompetitivenessLabel.TYPICAL_TO_STRONG: "Competitive Target",
                CompetitivenessLabel.CALL_TO_TYPICAL: "Within Reach with Strong CAT",
                CompetitivenessLabel.SLIGHTLY_BELOW_CALL: "High-Effort Target",
                CompetitivenessLabel.OUTSIDE_CURRENT_CALL_RANGE: "Aspirational Target — Keep Broader Options"
            }
        else:
            mapping = {
                CompetitivenessLabel.ABOVE_STRONG: "Comfortably Above Benchmark",
                CompetitivenessLabel.TYPICAL_TO_STRONG: "In Competitive Range",
                CompetitivenessLabel.CALL_TO_TYPICAL: "Around Call Range",
                CompetitivenessLabel.SLIGHTLY_BELOW_CALL: "Slightly Below Call Range",
                CompetitivenessLabel.OUTSIDE_CURRENT_CALL_RANGE: "Currently Outside Call Range"
            }
        return mapping.get(zone, "Unknown")
