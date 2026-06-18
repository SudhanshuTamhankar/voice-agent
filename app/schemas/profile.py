from typing import Optional
from pydantic import BaseModel

class ProfileDelta(BaseModel):
    """
    Represents the partial fields extracted from a single user message.
    Every field is optional because the user might only mention one or two things.
    """
    category: Optional[str] = None
    gender: Optional[str] = None
    class_10_score: Optional[float] = None
    class_12_score: Optional[float] = None
    graduation_score: Optional[float] = None
    graduation_stream: Optional[str] = None
    work_ex_months: Optional[int] = None
    target_exam: Optional[str] = None
    actual_percentile: Optional[float] = None

class UserProfile(BaseModel):
    """
    Represents the accumulated state of the user's profile across the session.
    """
    category: Optional[str] = None
    gender: Optional[str] = None
    class_10_score: Optional[float] = None
    class_12_score: Optional[float] = None
    graduation_score: Optional[float] = None
    graduation_stream: Optional[str] = None
    work_ex_months: Optional[int] = None
    target_exam: Optional[str] = None
    target_institute: Optional[str] = None
    actual_percentile: Optional[float] = None

    def merge_delta(self, delta: ProfileDelta):
        """
        Merges new incoming fields into the accumulated profile.
        Does not overwrite existing values with None.
        Auto-scales CGPA (scores <= 10.0) to percentage (* 10).
        """
        update_data = delta.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            # Auto-scale CGPA to percentage
            if key in ['class_10_score', 'class_12_score', 'graduation_score']:
                if isinstance(value, (int, float)) and value <= 10.0 and value > 0:
                    value = float(value) * 10.0
            
            setattr(self, key, value)

class GapCategory(str):
    FIXED = "FIXED"
    CONTROLLABLE = "CONTROLLABLE"

class ProfileGap(BaseModel):
    factor_name: str
    category: str  # FIXED or CONTROLLABLE
    points_lost: float
    description: str

class GapReport(BaseModel):
    biggest_fixed_bottleneck: Optional[ProfileGap] = None
    biggest_controllable_lever: Optional[ProfileGap] = None
    all_gaps: list[ProfileGap] = []

class CollegeBucket(str):
    STRONG = "STRONG"
    REALISTIC = "REALISTIC"
    STRETCH = "STRETCH"
    AMBITIOUS = "AMBITIOUS"
    UNLIKELY = "UNLIKELY"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

class CollegeRecommendation(BaseModel):
    institute_id: str
    bucket: str
    total_score: float
    safe_benchmark: float
    gap_from_safe: float
    is_mathematically_possible: bool

class RecommendationReport(BaseModel):
    strong_colleges: list[CollegeRecommendation] = []
    realistic_colleges: list[CollegeRecommendation] = []
    stretch_colleges: list[CollegeRecommendation] = []
    ambitious_colleges: list[CollegeRecommendation] = []
    unlikely_colleges: list[CollegeRecommendation] = []
    insufficient_data_colleges: list[str] = []
    gap_report: Optional[GapReport] = None

