from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class IIMACalculator(BaseCalculator):
    @property
    def institute_id(self) -> str:
        return "iim_ahmedabad"

    def _score_10th(self, score: float) -> float:
        if score <= 55: return 1.0
        if score <= 60: return 2.0
        if score <= 70: return 3.0
        if score <= 80: return 5.0
        if score <= 90: return 8.0
        return 10.0

    def _score_12th(self, score: float) -> float:
        # Simplified Science Stream
        if score <= 55: return 1.0
        if score <= 60: return 2.0
        if score <= 70: return 3.0
        if score <= 80: return 5.0
        if score <= 90: return 8.0
        return 10.0

    def _score_grad(self, score: float, stream: str) -> float:
        # Simplified Engineering (AC-4)
        if score <= 60: return 1.0
        if score <= 65: return 2.0
        if score <= 70: return 3.0
        if score <= 75: return 5.0
        if score <= 85: return 8.0
        return 10.0

    def _score_work_ex(self, months: int) -> float:
        if months <= 11:
            return 0.0
        pts = 0.20 * (months - 11)
        return min(pts, 5.0)

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        # 1. 10th Score
        s_10 = self._score_10th(profile.class_10_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="10th Score Rating",
            rule_cited="Rating Score A (Max 10)",
            score_awarded=s_10,
            max_possible_score=10.0,
            explanation=f"Awarded {s_10} points based on 10th score of {profile.class_10_score}%."
        ))

        # 2. 12th Score
        s_12 = self._score_12th(profile.class_12_score or 0)
        factors.append(FactorScoreTrace(
            factor_name="12th Score Rating",
            rule_cited="Rating Score B (Max 10)",
            score_awarded=s_12,
            max_possible_score=10.0,
            explanation=f"Awarded {s_12} points based on 12th score of {profile.class_12_score}%."
        ))

        # 3. Grad Score
        s_grad = self._score_grad(profile.graduation_score or 0, profile.graduation_stream or "Engineering")
        factors.append(FactorScoreTrace(
            factor_name="Graduation Score Rating",
            rule_cited="Rating Score C (Max 10)",
            score_awarded=s_grad,
            max_possible_score=10.0,
            explanation=f"Awarded {s_grad} points based on Graduation score of {profile.graduation_score}% in {profile.graduation_stream}."
        ))
        
        # 4. Work Ex
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        factors.append(FactorScoreTrace(
            factor_name="Work Experience",
            rule_cited="0.20 × (months - 11), max 5",
            score_awarded=round(s_work, 2),
            max_possible_score=5.0,
            explanation=f"Awarded {s_work} points for {profile.work_ex_months} months."
        ))

        # Calculate AR
        ar = s_10 + s_12 + s_grad + s_work
        factors.append(FactorScoreTrace(
            factor_name="Academic Rating (AR)",
            rule_cited="AR = A + B + C + Work Ex",
            score_awarded=ar,
            max_possible_score=35.0,
            explanation=f"Total AR is {ar}."
        ))

        # 5. CAT Score (Estimation)
        cat_pct = profile.actual_percentile
        if not cat_pct:
            s_cat = 0.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score",
                rule_cited="Scaled CAT Score",
                score_awarded=0.0,
                max_possible_score=204.0,
                explanation="No CAT percentile provided. Assuming 0 for calculation."
            ))
        else:
            s_cat = (cat_pct / 100.0) * 204.0
            factors.append(FactorScoreTrace(
                factor_name="CAT Score (Estimated Raw)",
                rule_cited="Estimated Scaled CAT Score",
                score_awarded=round(s_cat, 2),
                max_possible_score=204.0,
                explanation=f"Estimated raw score of {round(s_cat, 2)} based on {cat_pct} percentile."
            ))

        # 6. Composite Score
        # CS = 0.35*(AR/38) + 0.65*(CAT/204)  *Note: Max AR with no diversity is ~35, but formula divides by 38
        cs_ar_component = 0.35 * (ar / 38.0)
        cs_cat_component = 0.65 * (s_cat / 204.0)
        total_cs = (cs_ar_component + cs_cat_component) * 100  # Scale to 100 for benchmark comparison
        
        factors.append(FactorScoreTrace(
            factor_name="Composite Score (CS)",
            rule_cited="0.35 × (AR/38) + 0.65 × (CAT/204)",
            score_awarded=round(total_cs, 2),
            max_possible_score=100.0,
            explanation=f"Calculated final composite score scaled to 100."
        ))

        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=round(total_cs, 2),
            factors=factors
        )

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        # Calculate AR
        s_10 = self._score_10th(profile.class_10_score or 0)
        s_12 = self._score_12th(profile.class_12_score or 0)
        s_grad = self._score_grad(profile.graduation_score or 0, profile.graduation_stream or "Engineering")
        s_work = self._score_work_ex(profile.work_ex_months or 0)
        ar = s_10 + s_12 + s_grad + s_work

        target_cs_scaled = target_composite_score / 100.0
        ar_component = 0.35 * (ar / 38.0)
        required_cat_component = target_cs_scaled - ar_component

        if required_cat_component <= 0:
            # Reached target without CAT
            return 0.0
            
        required_cat_pct = (required_cat_component / 0.65) * 100.0
        
        if required_cat_pct > 100.0:
            return None # Mathematically impossible

        return round(required_cat_pct, 2)
