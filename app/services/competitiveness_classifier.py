from app.schemas.scoring import CompositeScoreResult, EvaluationResult, CompetitivenessLabel
from app.repositories.benchmark_repository import BenchmarkRepository

class CompetitivenessClassifier:
    def __init__(self, benchmark_repository: BenchmarkRepository):
        self.benchmark_repository = benchmark_repository

    def classify(self, score_result: CompositeScoreResult, category: str) -> EvaluationResult:
        benchmark = self.benchmark_repository.get_benchmark(score_result.institute_id, category)
        
        if not benchmark or not benchmark.raw_data:
            return EvaluationResult(
                institute_id=score_result.institute_id,
                composite_score=score_result.total_score,
                label=CompetitivenessLabel.INSUFFICIENT_DATA,
                factors=score_result.factors
            )

        # Extract thresholds
        raw = benchmark.raw_data
        call_threshold = raw.get("Call Threshold Composite")
        strong = raw.get("Strong Composite")
        
        # Determine Label
        label = CompetitivenessLabel.INSUFFICIENT_DATA
        score = score_result.total_score
        
        if call_threshold is not None and strong is not None:
            if score >= strong:
                label = CompetitivenessLabel.SAFE
            elif score >= call_threshold:
                label = CompetitivenessLabel.STRETCH
            else:
                label = CompetitivenessLabel.UNLIKELY

        return EvaluationResult(
            institute_id=score_result.institute_id,
            composite_score=score_result.total_score,
            label=label,
            safe_benchmark=strong,
            stretch_benchmark=call_threshold,
            factors=score_result.factors
        )
