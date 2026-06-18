from app.schemas.profile import UserProfile
from app.schemas.scoring import CompositeScoreResult, FactorScoreTrace
from app.services.calculators import get_calculator

class ProfileScoringEngine:
    def __init__(self):
        pass

    def calculate_score(self, profile: UserProfile, institute_id: str) -> CompositeScoreResult:
        """
        Delegates scoring to the specific python calculator for the institute.
        """
        calculator = get_calculator(institute_id)
        
        if not calculator:
            return CompositeScoreResult(
                institute_id=institute_id,
                total_score=0.0,
                factors=[FactorScoreTrace(
                    factor_name="Unknown",
                    rule_cited="No calculator available",
                    score_awarded=0.0,
                    explanation=f"A mathematical calculator has not been implemented for {institute_id} yet."
                )]
            )

        return calculator.calculate(profile)
