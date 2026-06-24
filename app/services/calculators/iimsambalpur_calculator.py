from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMSambalpurCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_sambalpur"

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # CAT Score scaled
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (self.cat_percentile_to_raw(profile.actual_percentile) / 130.0 * 100.0) * 0.40  # 0.31 overall + 0.09 for sections
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="Weighted CAT metrics",
                score_awarded=round(s_cat, 2),
                max_possible_score=40.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 40 based on {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="Weighted CAT metrics",
                score_awarded=0.0,
                max_possible_score=40.0,
                explanation="No CAT percentile provided."
            ))

        total_cs = s_cat
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        required_raw = target_composite_score / 0.40 * 130.0 / 100.0
        required_cat_pct = self.cat_raw_to_percentile(required_raw)
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
