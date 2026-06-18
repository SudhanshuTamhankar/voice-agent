from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMICalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_indore"

    def _score_10th(self, score: float) -> float:
        if score >= 90: return 10.0
        if score >= 80: return 8.0
        if score >= 70: return 6.0
        return 4.0

    def _score_12th(self, score: float) -> float:
        if score >= 90: return 25.0
        if score >= 80: return 20.0
        if score >= 70: return 15.0
        return 10.0

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

        # 3. 12th Score (Weight 25)
        s_12 = self._score_12th(profile.class_12_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="12th Score",
            rule_cited="12th Weight 25",
            score_awarded=s_12,
            max_possible_score=25.0,
            explanation=f"Awarded {s_12} points."
        ))

        # 4. Diversity Factors (Weight 7)
        s_div = 7.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Diversity",
            rule_cited="Diversity Weight 7",
            score_awarded=s_div,
            max_possible_score=7.0,
            explanation=f"Awarded {s_div} points for diversity."
        ))

        # 5. Work Ex (Weight 3)
        s_work = 0.0 # Approximation since it says 0-3
        if profile.work_ex_months:
            s_work = min((profile.work_ex_months / 36.0) * 3.0, 3.0)
            
        factors.append(FactorScoreTrace(
            factor_name="Work Experience",
            rule_cited="Work Ex Weight 3",
            score_awarded=round(s_work, 2),
            max_possible_score=3.0,
            explanation=f"Awarded {round(s_work, 2)} points."
        ))

        total_cs = s_cat + s_10 + s_12 + s_div + s_work
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_10 = self._score_10th(profile.class_10_score or 0)
        s_12 = self._score_12th(profile.class_12_score or 0)
        s_div = 7.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        
        s_work = 0.0
        if profile.work_ex_months:
            s_work = min((profile.work_ex_months / 36.0) * 3.0, 3.0)

        profile_score = s_10 + s_12 + s_div + s_work
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_cat_pct = (required_cat_component / 55.0) * 100.0
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
