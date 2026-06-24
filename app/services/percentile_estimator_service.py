from app.schemas.profile import UserProfile
from app.repositories.benchmark_repository import BenchmarkRepository
from app.services.calculators import get_calculator

class PercentileTargetResult:
    def __init__(
        self,
        institute_id: str,
        category: str,
        is_possible: bool,
        percentile_range: str | None = None,
        explanation: str = ""
    ):
        self.institute_id = institute_id
        self.category = category
        self.is_possible = is_possible
        self.percentile_range = percentile_range
        self.explanation = explanation

class PercentileEstimatorService:
    def __init__(self, benchmark_repo: BenchmarkRepository):
        self.benchmark_repo = benchmark_repo

    def estimate_target(self, profile: UserProfile, institute_id: str) -> PercentileTargetResult:
        """
        Calculates the required CAT percentile range using the TC formula.
        TC = 0.5M + 0.3H + 0.2T
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

        raw = benchmark.raw_data or {}
        T = raw.get("Call Threshold Composite")
        M = raw.get("Typical Successful Composite")
        H = raw.get("Strong Composite")
        
        if T is not None and M is not None and H is not None:
            target_cs = (0.5 * M) + (0.3 * H) + (0.2 * T)
        else:
            target_cs = benchmark.composite_score_safe or benchmark.composite_score_stretch
            
        if target_cs is None:
             return PercentileTargetResult(
                institute_id=institute_id,
                category=category,
                is_possible=False,
                explanation="No target composite score benchmark available for this institute to reverse-engineer."
            )

        # Reverse engineer using the Target Score
        required_pct = calculator.estimate_required_percentile(profile, target_cs)

        if required_pct is None:
            if institute_id in ["xlri_jamshedpur", "nmims_mumbai", "sibm_pune", "jbims_mumbai", "isb_hyderabad", "spjimr_mumbai", "iim_ranchi", "iifm_bhopal"]:
                return PercentileTargetResult(
                    institute_id=institute_id,
                    category=category,
                    is_possible=True,
                    explanation="This institute relies primarily on exam scores or opaque profile reviews, rather than a mathematical composite score. Aim for the highest possible percentile in its respective exam."
                )
            else:
                # Check if they can at least reach the minimum threshold
                threshold_pct = None
                if T is not None:
                    threshold_pct = calculator.estimate_required_percentile(profile, T)
                
                if threshold_pct is not None:
                    return PercentileTargetResult(
                        institute_id=institute_id,
                        category=category,
                        is_possible=False,
                        explanation=f"Based on your fixed academic profile, you can reach the minimum call threshold with a CAT percentile around {threshold_pct:.1f}. However, it is mathematically impossible to reach the higher 'Safe/Strong' target composite tier even with a 100 percentile in CAT."
                    )
                else:
                    return PercentileTargetResult(
                        institute_id=institute_id,
                        category=category,
                        is_possible=False,
                        explanation="Based on your fixed academic profile and work experience, it is mathematically impossible to reach even the minimum call threshold target even with a 100 percentile in CAT."
                    )

        range_str = f"{max(0.0, required_pct - 0.2):.1f}–{min(100.0, required_pct + 0.2):.1f}"
        return PercentileTargetResult(
            institute_id=institute_id,
            category=category,
            is_possible=True,
            percentile_range=range_str,
            explanation="Calculation successful based on the institute's composite-score logic."
        )
