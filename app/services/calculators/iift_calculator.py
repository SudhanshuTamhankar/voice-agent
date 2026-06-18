from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIFTCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iift_delhi"

    def _score_work_ex(self, months: int) -> float:
        if months >= 36:
            return 5.0
        return (5.0 * months) / 36.0

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. CAT Score (Weight 90)
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (profile.actual_percentile / 100.0) * 90.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 90",
                score_awarded=round(s_cat, 2),
                max_possible_score=90.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 90."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 90",
                score_awarded=0.0,
                max_possible_score=90.0,
                explanation="No CAT percentile provided."
            ))

        # 2. Work Ex (Weight 5)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        factors.append(FactorScoreTrace(
            factor_name="Work Experience",
            rule_cited="Work Experience Weight 5",
            score_awarded=round(s_work, 2),
            max_possible_score=5.0,
            explanation=f"Awarded {round(s_work, 2)} points."
        ))

        # 3. Gender Diversity (Weight 5)
        s_gender = 5.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Gender Diversity",
            rule_cited="Gender Weight 5",
            score_awarded=s_gender,
            max_possible_score=5.0,
            explanation=f"Awarded {s_gender} points for gender: {profile.gender}."
        ))

        total_cs = s_cat + s_work + s_gender
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        s_gender = 5.0 if profile.gender and profile.gender.lower() == "female" else 0.0

        profile_score = s_work + s_gender
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_cat_pct = (required_cat_component / 90.0) * 100.0
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
