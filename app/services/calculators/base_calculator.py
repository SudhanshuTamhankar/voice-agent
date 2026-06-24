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

    def cat_percentile_to_raw(self, pct: float) -> float:
        """
        Approximates CAT raw score (out of 198) from percentile.
        100%ile -> 130
        99.9%ile -> 110
        99.0%ile -> 85
        95.0%ile -> 60
        90.0%ile -> 45
        80.0%ile -> 35
        """
        if pct <= 0: return 0.0
        if pct >= 100: return 130.0 # Using max achieved score as denominator for raw ratio
        
        # Simple polynomial interpolation for realistic CAT curve
        if pct >= 99.9: return 110.0 + (pct - 99.9) * 200.0 # 99.9 to 100 maps to 110-130
        if pct >= 99.0: return 85.0 + (pct - 99.0) * (25.0 / 0.9)
        if pct >= 95.0: return 60.0 + (pct - 95.0) * (25.0 / 4.0)
        if pct >= 90.0: return 45.0 + (pct - 90.0) * (15.0 / 5.0)
        if pct >= 80.0: return 35.0 + (pct - 90.0) * (10.0 / 10.0)
        return pct * 0.4375 # 80 maps to 35

    def cat_raw_to_percentile(self, raw: float) -> float:
        if raw >= 130: return 100.0
        if raw >= 110: return 99.9 + (raw - 110) * (0.1 / 20.0)
        if raw >= 85: return 99.0 + (raw - 85) * (0.9 / 25.0)
        if raw >= 60: return 95.0 + (raw - 60) * (4.0 / 25.0)
        if raw >= 45: return 90.0 + (raw - 45) * (5.0 / 15.0)
        if raw >= 35: return 80.0 + (raw - 35) * (10.0 / 10.0)
        if raw <= 0: return 0.0
        return raw / 0.4375
