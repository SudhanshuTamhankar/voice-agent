from abc import ABC, abstractmethod
from typing import List
from app.schemas.profile import UserProfile
from app.schemas.scoring import FactorScoreTrace, CompositeScoreResult

class BaseCalculator(ABC):
    @property
    @abstractmethod
    def institute_id(self) -> str:
        """Return the ID of the institute this calculator handles (e.g. 'iim_ahmedabad')."""
        pass

    @abstractmethod
    def calculate(self, profile: UserProfile) -> CompositeScoreResult:
        """
        Takes the user profile and calculates the mathematically deterministic
        score based on the specific institute's rules.
        """
        pass

    def estimate_required_percentile(self, profile: UserProfile, target_composite_score: float) -> float | None:
        """
        Calculates the required CAT percentile to achieve the target_composite_score,
        given the user's fixed profile parameters (Academics, Work Ex, Diversity).
        Returns None if it is mathematically impossible to reach the score, or if 
        the institute does not use a deterministic mathematical formula.
        """
        return None
