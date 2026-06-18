from pydantic import BaseModel, Field
from typing import Optional

class Factor(BaseModel):
    institute_name: str = Field(alias="Institute_Name")
    factor_name: str = Field(alias="Factor_Name")
    factor_category: Optional[str] = Field(None, alias="Factor_Category")
    published_value: Optional[str] = Field(None, alias="Published_Value")
    published_unit: Optional[str] = Field(None, alias="Published_Unit")
    formula: Optional[str] = Field(None, alias="Formula")
    mandatory: Optional[str] = Field(None, alias="Mandatory")
    verification_status: Optional[str] = Field(None, alias="Verification_Status")
    admission_cycle: Optional[str] = Field(None, alias="Admission_Cycle")
    source_type: Optional[str] = Field(None, alias="Source_Type")
    source_reference: Optional[str] = Field(None, alias="Source_Reference")
    
    @property
    def institute_id(self) -> str:
        return self.institute_name.lower().replace(" ", "_").replace("-", "_")
