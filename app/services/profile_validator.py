from typing import List
from app.schemas.profile import UserProfile

class ProfileValidator:
    """
    Checks if a UserProfile has all mandatory fields required for deterministic scoring.
    """
    REQUIRED_FIELDS = [
        "category", 
        "gender", 
        "class_10_score", 
        "class_12_score", 
        "graduation_score", 
        "graduation_stream",
        "work_ex_months"
    ]

    @classmethod
    def get_missing_fields(cls, profile: UserProfile, require_exam_score: bool = False) -> List[str]:
        missing = []
        for field in cls.REQUIRED_FIELDS:
            # Check if attribute is None. Note: 0 is a valid value for work_ex_months.
            if getattr(profile, field) is None:
                missing.append(field)
                
        if require_exam_score and profile.actual_percentile is None:
            missing.append("actual_percentile")
            
        return missing
