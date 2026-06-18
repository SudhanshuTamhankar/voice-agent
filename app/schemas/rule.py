from pydantic import BaseModel, Field
from typing import Optional

class ScoringRule(BaseModel):
    institute_name: str = Field(alias="Institute_Name")
    factor: str = Field(alias="Factor")
    weightage: Optional[str] = Field(None, alias="Weightage")
    unit: Optional[str] = Field(None, alias="Unit")
    formula: Optional[str] = Field(None, alias="Formula")
    minimum_requirement: Optional[str] = Field(None, alias="Minimum_Requirement")
    maximum_score: Optional[str] = Field(None, alias="Maximum_Score")
    verified: Optional[str] = Field(None, alias="Verified")

    @property
    def institute_id(self) -> str:
        return self.institute_name.lower().replace(" ", "_").replace("-", "_")
