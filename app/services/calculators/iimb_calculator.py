from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMBCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_bangalore"

    def _score_10th(self, score: float) -> float:
        # Standardized approximation for 10 points
        if score <= 60: return 2.0
        if score <= 70: return 4.0
        if score <= 80: return 6.0
        if score <= 90: return 8.0
        return 10.0

    def _score_12th(self, score: float) -> float:
        if score <= 60: return 2.0
        if score <= 70: return 4.0
        if score <= 80: return 6.0
        if score <= 90: return 8.0
        return 10.0

    def _score_grad(self, score: float) -> float:
        if score <= 60: return 2.0
        if score <= 70: return 4.0
        if score <= 80: return 6.0
        if score <= 85: return 8.0
        return 10.0

    def _score_work_ex(self, months: int) -> float:
        if months >= 36:
            return 10.0
        return (10.0 * months) / 36.0

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. CAT Score (Weight 55)
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (profile.actual_percentile / 100.0) * 55.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 55",
                score_awarded=round(s_cat, 2),
                max_possible_score=55.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 55 based on {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 55",
                score_awarded=0.0,
                max_possible_score=55.0,
                explanation="No CAT percentile provided."
            ))

        # 2. 10th Score (Weight 10)
        s_10 = self._score_10th(profile.class_10_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="10th Score",
            rule_cited="10th Weight 10",
            score_awarded=s_10,
            max_possible_score=10.0,
            explanation=f"Awarded {s_10} points."
        ))

        # 3. 12th Score (Weight 10)
        s_12 = self._score_12th(profile.class_12_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="12th Score",
            rule_cited="12th Weight 10",
            score_awarded=s_12,
            max_possible_score=10.0,
            explanation=f"Awarded {s_12} points."
        ))

        # 4. Grad Score (Weight 10)
        s_grad = self._score_grad(profile.graduation_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="Graduation Score",
            rule_cited="Bachelor Weight 10",
            score_awarded=s_grad,
            max_possible_score=10.0,
            explanation=f"Awarded {s_grad} points."
        ))
        
        # 5. Work Ex (Weight 10)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        factors.append(FactorScoreTrace(
            factor_name="Work Experience",
            rule_cited="10x/36 for x<36; 10 at x>=36",
            score_awarded=round(s_work, 2),
            max_possible_score=10.0,
            explanation=f"Awarded {round(s_work, 2)} points for {profile.work_ex_months} months."
        ))
        
        # 6. Gender Diversity (Weight 5)
        s_gender = 5.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Gender Diversity",
            rule_cited="Gender Weight 5",
            score_awarded=s_gender,
            max_possible_score=5.0,
            explanation=f"Awarded {s_gender} points for gender: {profile.gender}."
        ))

        total_cs = s_cat + s_10 + s_12 + s_grad + s_work + s_gender
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_10 = self._score_10th(profile.class_10_score or 0)
        s_12 = self._score_12th(profile.class_12_score or 0)
        s_grad = self._score_grad(profile.graduation_score or 0)
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        s_gender = 5.0 if profile.gender and profile.gender.lower() == "female" else 0.0

        profile_score = s_10 + s_12 + s_grad + s_work + s_gender
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_cat_pct = (required_cat_component / 55.0) * 100.0
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
