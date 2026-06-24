from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class CompetitivenessLabel(str, Enum):
    ABOVE_STRONG = "ABOVE_STRONG"
    TYPICAL_TO_STRONG = "TYPICAL_TO_STRONG"
    CALL_TO_TYPICAL = "CALL_TO_TYPICAL"
    SLIGHTLY_BELOW_CALL = "SLIGHTLY_BELOW_CALL"
    OUTSIDE_CURRENT_CALL_RANGE = "OUTSIDE_CURRENT_CALL_RANGE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

class EvaluationMode(str, Enum):
    PRE_CAT = "PRE_CAT"
    SCORE_KNOWN = "SCORE_KNOWN"

class FactorScoreTrace(BaseModel):
    factor_name: str = Field(..., description="The name of the factor being evaluated (e.g., 'Class 10', 'Work experience').")
    rule_cited: str = Field(..., description="The exact rule text or formula from the dataset used to make this decision.")
    score_awarded: float = Field(..., description="The exact mathematical points awarded based on the profile and rule. Use 0.0 if not applicable or no points awarded.")
    max_possible_score: Optional[float] = Field(None, description="The maximum possible score for this factor, if explicitly stated in the rule.")
    explanation: str = Field(..., description="A short logical explanation of why this score was awarded.")

class DynamicScoringOutput(BaseModel):
    factors: List[FactorScoreTrace] = Field(..., description="The list of evaluated factor scores.")

class CompositeScoreResult(BaseModel):
    institute_id: str
    total_score: float
    factors: List[FactorScoreTrace]
    
class EvaluationResult(BaseModel):
    institute_id: str
    composite_score: float
    mode: EvaluationMode
    zone: CompetitivenessLabel
    user_facing_label: str
    strengths: str = ""
    risks: str = ""
    next_action: str = ""
    factors: List[FactorScoreTrace]
