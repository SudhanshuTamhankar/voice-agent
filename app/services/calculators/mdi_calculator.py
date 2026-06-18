from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class MDICalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "mdi_gurgaon"

    def _score_acad(self, score: float, weight: float) -> float:
        if score >= 90: return weight
        if score >= 80: return weight * 0.8
        if score >= 70: return weight * 0.6
        return weight * 0.4

    def _score_work_ex(self, months: int) -> float:
        if months >= 36: return 10.0
        return (10.0 * months) / 36.0

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. CAT Score (Weight 70)
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (profile.actual_percentile / 100.0) * 70.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 70",
                score_awarded=round(s_cat, 2),
                max_possible_score=70.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 70 based on {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 70",
                score_awarded=0.0,
                max_possible_score=70.0,
                explanation="No CAT percentile provided."
            ))

        # 2. 10th Score (Weight 5)
        s_10 = self._score_acad(profile.class_10_score or 0, 5.0)
        factors.append(FactorScoreTrace(
            factor_name="10th Score",
            rule_cited="10th Weight 5",
            score_awarded=round(s_10, 2),
            max_possible_score=5.0,
            explanation=f"Awarded {round(s_10, 2)} points."
        ))

        # 3. 12th Score (Weight 5)
        s_12 = self._score_acad(profile.class_12_score or 0, 5.0)
        factors.append(FactorScoreTrace(
            factor_name="12th Score",
            rule_cited="12th Weight 5",
            score_awarded=round(s_12, 2),
            max_possible_score=5.0,
            explanation=f"Awarded {round(s_12, 2)} points."
        ))

        # 4. Grad Score (Weight 5)
        s_grad = self._score_acad(profile.graduation_score or 0, 5.0)
        factors.append(FactorScoreTrace(
            factor_name="Graduation Score",
            rule_cited="Grad Weight 5",
            score_awarded=round(s_grad, 2),
            max_possible_score=5.0,
            explanation=f"Awarded {round(s_grad, 2)} points."
        ))

        # 5. Work Ex (Weight 10)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        factors.append(FactorScoreTrace(
            factor_name="Work Experience",
            rule_cited="Work Experience Weight 10",
            score_awarded=round(s_work, 2),
            max_possible_score=10.0,
            explanation=f"Awarded {round(s_work, 2)} points."
        ))

        # 6. Diversity Factors (Weight 5 Total)
        s_div = 2.5 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Diversity",
            rule_cited="Gender Diversity 2.5 + Acad 2.5",
            score_awarded=s_div,
            max_possible_score=5.0,
            explanation=f"Awarded {s_div} points for diversity."
        ))

        total_cs = s_cat + s_10 + s_12 + s_grad + s_work + s_div
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_10 = self._score_acad(profile.class_10_score or 0, 5.0)
        s_12 = self._score_acad(profile.class_12_score or 0, 5.0)
        s_grad = self._score_acad(profile.graduation_score or 0, 5.0)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        s_div = 2.5 if profile.gender and profile.gender.lower() == "female" else 0.0

        profile_score = s_10 + s_12 + s_grad + s_work + s_div
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_cat_pct = (required_cat_component / 70.0) * 100.0
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
