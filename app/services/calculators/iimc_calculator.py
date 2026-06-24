from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMCCalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_calcutta"

    def _score_10th(self, score: float) -> float:
        if score >= 80: return 10.0
        if score >= 75: return 8.0
        if score >= 70: return 6.0
        if score >= 65: return 4.0
        if score >= 60: return 2.0
        return 0.0

    def _score_12th(self, score: float) -> float:
        if score >= 80: return 15.0
        if score >= 75: return 12.0
        if score >= 70: return 9.0
        if score >= 65: return 6.0
        if score >= 60: return 3.0
        return 0.0

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. CAT Score (Weight 56)
        s_cat = 0.0
        if profile.actual_percentile:
            s_cat = (self.cat_percentile_to_raw(profile.actual_percentile) / 130.0) * 56.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 56",
                score_awarded=round(s_cat, 2),
                max_possible_score=56.0,
                explanation=f"Estimated {round(s_cat, 2)} points out of 56 based on {profile.actual_percentile} percentile."
            ))
        else:
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="CAT Weight 56",
                score_awarded=0.0,
                max_possible_score=56.0,
                explanation="No CAT percentile provided."
            ))

        # 2. 10th Score (Weight 10)
        s_10 = self._score_10th(profile.class_10_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="10th Score",
            rule_cited="10/8/6/4/2/0",
            score_awarded=s_10,
            max_possible_score=10.0,
            explanation=f"Awarded {s_10} points."
        ))

        # 3. 12th Score (Weight 15)
        s_12 = self._score_12th(profile.class_12_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="12th Score",
            rule_cited="15/12/9/6/3/0",
            score_awarded=s_12,
            max_possible_score=15.0,
            explanation=f"Awarded {s_12} points."
        ))
        
        # 4. Gender Diversity (Weight 4)
        s_gender = 4.0 if profile.gender and profile.gender.lower() == "female" else 0.0
        factors.append(FactorScoreTrace(
            factor_name="Gender Diversity",
            rule_cited="Gender Weight 4",
            score_awarded=s_gender,
            max_possible_score=4.0,
            explanation=f"Awarded {s_gender} points for gender: {profile.gender}."
        ))

        total_cs = s_cat + s_10 + s_12 + s_gender
        
        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        s_10 = self._score_10th(profile.class_10_score or 0)
        s_12 = self._score_12th(profile.class_12_score or 0)
        s_gender = 4.0 if profile.gender and profile.gender.lower() == "female" else 0.0

        profile_score = s_10 + s_12 + s_gender
        required_cat_component = target_composite_score - profile_score

        if required_cat_component <= 0:
            return 0.0
            
        required_raw = (required_cat_component / 56.0) * 130.0
        required_cat_pct = self.cat_raw_to_percentile(required_raw)
        
        if required_cat_pct > 100.0:
            return None

        return round(required_cat_pct, 2)
