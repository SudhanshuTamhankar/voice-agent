from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMShillongCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_shillong"

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # CAT Score scaled (65%)
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (self.cat_percentile_to_raw(profile.actual_percentile) / 130.0) * 65.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 65",
                score_awarded=round(s_cat, 2),
                max_possible_score=65.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 65 based on {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 65",
                score_awarded=0.0,
                max_possible_score=65.0,
                explanation="No CAT percentile provided."
            ))

        # Academics (35%)
        # Estimating simple average of 10th and 12th
        s_10 = profile.class_10_score or 0.0
        s_12 = profile.class_12_score or 0.0
        s_acad = ((s_10 + s_12) / 200.0) * 35.0
        
        factors.append(FactorScoreTrace(
            factor_name="Academic Score",
            rule_cited="NARS Weight 35",
            score_awarded=round(s_acad, 2),
            max_possible_score=35.0,
            explanation=f"Estimated {round(s_acad, 2)} points out of 35 based on 10th and 12th scores."
        ))

        total_cs = s_cat + s_acad
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_10 = profile.class_10_score or 0.0
        s_12 = profile.class_12_score or 0.0
        profile_score = ((s_10 + s_12) / 200.0) * 35.0

        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_raw = (required_cat_component / 65.0) * 130.0
        required_cat_pct = self.cat_raw_to_percentile(required_raw)
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
