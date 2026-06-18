from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult
from .base_calculator import BaseCalculator

class GenericExamCalculator(BaseCalculator):
    """
    A generic passthrough calculator for institutes that do not use a 
    deterministic multi-factor profile formula, but rather rely 100% on 
    an exam score (like XAT/NMAT) or an opaque profile review.
    """
    def __init__(self, institute_id: str, explanation: str):
        self._institute_id = institute_id
        self._explanation = explanation

    @property
    def institute_id(self) -> str:
        return self._institute_id

    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        factors: List[FactorScoreTrace] = []
        
        factors.append(FactorScoreTrace(
            factor_name="Exam/Opaque Selection",
            rule_cited="No published deterministic formula",
            score_awarded=0.0,
            max_possible_score=100.0,
            explanation=self._explanation
        ))

        return CompositeScoreResult(
            institute_id=self.institute_id,
            total_score=0.0,
            factors=factors
        )
