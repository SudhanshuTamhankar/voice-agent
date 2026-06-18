from pydantic import BaseModel, Field
from typing import List, Optional

class KnowledgeBaseEntry(BaseModel):
    institute: str = Field(alias="Institute")
    shortlisting_methodology: Optional[str] = Field(None, alias="Shortlisting_Methodology")
    key_factors: List[str] = Field(default_factory=list, alias="Key_Factors")
    academic_evaluation: Optional[str] = Field(None, alias="Academic_Evaluation")
    work_experience_evaluation: Optional[str] = Field(None, alias="Work_Experience_Evaluation")
    diversity_evaluation: Optional[str] = Field(None, alias="Diversity_Evaluation")
    professional_qualification_rules: Optional[str] = Field(None, alias="Professional_Qualification_Rules")
    important_exceptions: List[str] = Field(default_factory=list, alias="Important_Exceptions")
    formula_summary: Optional[str] = Field(None, alias="Formula_Summary")
    confidence: Optional[str] = Field(None, alias="Confidence")

    @property
    def institute_id(self) -> str:
        return self.institute.lower().replace(" ", "_").replace("-", "_")
