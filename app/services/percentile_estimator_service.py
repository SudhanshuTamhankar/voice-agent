from app.schemas.profile import UserProfile
from app.repositories.benchmark_repository import BenchmarkRepository
from app.services.calculators import get_calculator

class PercentileTargetResult:
    def __init__(
        self,
        institute_id: str,
        category: str,
        is_possible: bool,
        required_percentile: float | None = None,
        explanation: str = ""
    ):
        self.institute_id = institute_id
        self.category = category
        self.is_possible = is_possible
        self.required_percentile = required_percentile
        self.explanation = explanation

class PercentileEstimatorService:
    def __init__(self, benchmark_repo: BenchmarkRepository):
        self.benchmark_repo = benchmark_repo

    def estimate_target(self, profile: UserProfile, institute_id: str) -> PercentileTargetResult:
        """
        Calculates the required CAT percentile to hit the safe benchmark for the given institute.
        """
        category = profile.category or "General"
        benchmark = self.benchmark_repo.get_benchmark(institute_id, category)
        
        if not benchmark:
            return PercentileTargetResult(
                institute_id=institute_id,
                category=category,
                is_possible=False,
                explanation="No benchmark data available for this institute and category."
            )

        calculator = get_calculator(institute_id)
        if not calculator:
            return PercentileTargetResult(
                institute_id=institute_id,
                category=category,
                is_possible=False,
                explanation="No calculation engine available for this institute."
            )

        target_cs = benchmark.composite_score_safe or benchmark.composite_score_stretch
        
        if target_cs is None:
             return PercentileTargetResult(
                institute_id=institute_id,
                category=category,
                is_possible=False,
                explanation="No target composite score benchmark available for this institute to reverse-engineer."
            )

        # Reverse engineer using the Safe Score
        required_pct = calculator.estimate_required_percentile(profile, target_cs)

        if required_pct is None:
            # It's either impossible, or it's a GenericExamCalculator
            if institute_id in ["xlri_jamshedpur", "nmims_mumbai", "sibm_pune", "jbims_mumbai", "isb_hyderabad", "spjimr_mumbai", "iim_ranchi", "iifm_bhopal"]:
                return PercentileTargetResult(
                    institute_id=institute_id,
                    category=category,
                    is_possible=True,
                    # We could fetch the exact exam cutoff here if we had it in benchmarks, but for now we explain
                    explanation="This institute relies primarily on exam scores or opaque profile reviews, rather than a mathematical composite score. Aim for the highest possible percentile in its respective exam."
                )
            else:
                return PercentileTargetResult(
                    institute_id=institute_id,
                    category=category,
                    is_possible=False,
                    explanation="Based on your current academic and work experience profile, it is mathematically impossible to reach the required safe score even with a 100 percentile in CAT."
                )

        return PercentileTargetResult(
            institute_id=institute_id,
            category=category,
            is_possible=True,
            required_percentile=required_pct,
            explanation=f"To reach the safe composite score of {target_cs}, you need to target approximately {required_pct} percentile."
        )
