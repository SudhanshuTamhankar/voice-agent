from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class FMSCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "fms_delhi"

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. CAT Score (Weight 100 scaled from sections)
        # FMS uses 40% VARC, 30% DILR, 30% QA. Since we only have overall, we use 100%.
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (profile.actual_percentile / 100.0) * 100.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="40% VARC + 30% DILR + 30% QA",
                score_awarded=round(s_cat, 2),
                max_possible_score=100.0,
                explanation=f"Estimated {round(s_cat, 2)} points based on overall {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="40% VARC + 30% DILR + 30% QA",
                score_awarded=0.0,
                max_possible_score=100.0,
                explanation="No CAT percentile provided."
            ))

        # 2. Gender Diversity (Bonus 5)
        s_gender = 5.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Gender Diversity",
            rule_cited="Women Bonus 5",
            score_awarded=s_gender,
            max_possible_score=5.0,
            explanation=f"Awarded {s_gender} points for gender: {profile.gender}."
        ))

        total_cs = s_cat + s_gender
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_gender = 5.0 if profile.gender and profile.gender.lower() == "female" else 0.0

        profile_score = s_gender
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_cat_pct = required_cat_component
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
