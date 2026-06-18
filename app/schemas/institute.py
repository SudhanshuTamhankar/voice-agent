from pydantic import BaseModel, Field
from typing import Optional

class Institute(BaseModel):
    institute_name: str = Field(alias="Institute_Name")
    institute_type: Optional[str] = Field(None, alias="Institute_Type")
    entrance_exam: Optional[str] = Field(None, alias="Entrance_Exam")
    admission_cycle: Optional[str] = Field(None, alias="Admission_Cycle")
    verification_status: Optional[str] = Field(None, alias="Verification_Status")
    confidence_level: Optional[str] = Field(None, alias="Confidence_Level")
    source_type: Optional[str] = Field(None, alias="Source_Type")
    shortlisting_pathway: Optional[str] = Field(None, alias="Shortlisting_Pathway")
    shortlisting_formula: Optional[str] = Field(None, alias="Shortlisting_Formula")
    remarks: Optional[str] = Field(None, alias="Remarks")
    
    @property
    def institute_id(self) -> str:
        # Generate a stable canonical ID from the name (e.g., "IIM Ahmedabad" -> "iim_ahmedabad")
        return self.institute_name.lower().replace(" ", "_").replace("-", "_")
