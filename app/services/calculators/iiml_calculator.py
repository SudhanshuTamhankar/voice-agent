from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMLCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_lucknow"

    def _score_12th(self, score: float) -> float:
        if score >= 90: return 10.0
        if score >= 85: return 8.0
        if score >= 80: return 6.0
        return 4.0

    def _score_grad(self, score: float) -> float:
        if score >= 85: return 10.0
        if score >= 80: return 8.0
        if score >= 75: return 6.0
        return 4.0

    def _score_work_ex(self, months: int) -> float:
        if months < 6: return 0.0
        if months >= 24: return 10.0
        return (10.0 * (months - 6)) / 18.0

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. CAT Score (Weight 60)
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (profile.actual_percentile / 100.0) * 60.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 60",
                score_awarded=round(s_cat, 2),
                max_possible_score=60.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 60 based on {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 60",
                score_awarded=0.0,
                max_possible_score=60.0,
                explanation="No CAT percentile provided."
            ))

        # 2. 12th Score (Weight 10)
        s_12 = self._score_12th(profile.class_12_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="12th Score",
            rule_cited="12th Weight 10",
            score_awarded=s_12,
            max_possible_score=10.0,
            explanation=f"Awarded {s_12} points."
        ))

        # 3. Grad Score (Weight 10)
        s_grad = self._score_grad(profile.graduation_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="Graduation Score",
            rule_cited="Graduation Weight 10",
            score_awarded=s_grad,
            max_possible_score=10.0,
            explanation=f"Awarded {s_grad} points."
        ))

        # 4. Work Ex (Weight 10)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        factors.append(FactorScoreTrace(
            factor_name="Work Experience",
            rule_cited="Work Experience Weight 10",
            score_awarded=round(s_work, 2),
            max_possible_score=10.0,
            explanation=f"Awarded {round(s_work, 2)} points."
        ))

        # 5. Diversity Factors (Weight 10)
        s_div = 10.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Diversity",
            rule_cited="Diversity Factors 10",
            score_awarded=s_div,
            max_possible_score=10.0,
            explanation=f"Awarded {s_div} points for diversity."
        ))

        total_cs = s_cat + s_12 + s_grad + s_work + s_div
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_12 = self._score_12th(profile.class_12_score or 0)
        s_grad = self._score_grad(profile.graduation_score or 0)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        s_div = 10.0 if profile.gender and profile.gender.lower() == "female" else 0.0

        profile_score = s_12 + s_grad + s_work + s_div
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_cat_pct = (required_cat_component / 60.0) * 100.0
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
