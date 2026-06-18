from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMKCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_kozhikode"

    def _score_10th(self, score: float) -> float:
        return (score / 100.0) * 15.0

    def _score_12th(self, score: float) -> float:
        return (score / 100.0) * 20.0

    def _score_work_ex(self, months: int) -> float:
        if months >= 36: return 5.0
        return (5.0 * months) / 36.0

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. CAT Score (Weight 50)
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (profile.actual_percentile / 100.0) * 50.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 50",
                score_awarded=round(s_cat, 2),
                max_possible_score=50.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 50 based on {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 50",
                score_awarded=0.0,
                max_possible_score=50.0,
                explanation="No CAT percentile provided."
            ))

        # 2. 10th Score (Weight 15)
        s_10 = self._score_10th(profile.class_10_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="10th Score",
            rule_cited="10th Weight 15",
            score_awarded=round(s_10, 2),
            max_possible_score=15.0,
            explanation=f"Awarded {round(s_10, 2)} points."
        ))

        # 3. 12th Score (Weight 20)
        s_12 = self._score_12th(profile.class_12_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="12th Score",
            rule_cited="12th Weight 20",
            score_awarded=round(s_12, 2),
            max_possible_score=20.0,
            explanation=f"Awarded {round(s_12, 2)} points."
        ))

        # 4. Work Ex (Weight 5)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        factors.append(FactorScoreTrace(
            factor_name="Work Experience",
            rule_cited="Work Experience Weight 5",
            score_awarded=round(s_work, 2),
            max_possible_score=5.0,
            explanation=f"Awarded {round(s_work, 2)} points."
        ))

        # 5. Diversity Factors (Weight 10)
        s_div = 10.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Diversity",
            rule_cited="Gender/Academic Diversity Weight 10",
            score_awarded=s_div,
            max_possible_score=10.0,
            explanation=f"Awarded {s_div} points for diversity."
        ))

        total_cs = s_cat + s_10 + s_12 + s_work + s_div
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_10 = self._score_10th(profile.class_10_score or 0)
        s_12 = self._score_12th(profile.class_12_score or 0)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        s_div = 10.0 if profile.gender and profile.gender.lower() == "female" else 0.0

        profile_score = s_10 + s_12 + s_work + s_div
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_cat_pct = (required_cat_component / 50.0) * 100.0
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
