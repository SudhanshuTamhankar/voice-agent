from pydantic import BaseModel, Field
from typing import Optional

class Benchmark(BaseModel):
    institute_name: str = Field(alias="Institute")
    category: str = Field(alias="Category")
    
    # Keeping it flexible since we haven't seen exact columns of the excel file yet.
    # The repository will map the raw row dict into this schema.
    composite_score_safe: Optional[float] = Field(None, alias="Typical Successful Composite")
    composite_score_stretch: Optional[float] = Field(None, alias="Call Threshold Composite")
    cat_percentile_safe: Optional[float] = Field(None, alias="Typical Successful CAT")
    cat_percentile_stretch: Optional[float] = Field(None, alias="Call Threshold CAT")
    
    confidence_score: Optional[str] = Field(None, alias="Confidence Score")
    confidence_explanation: Optional[str] = Field(None, alias="Confidence Explanation")
    
    raw_data: Optional[dict] = None

    @property
    def institute_id(self) -> str:
        return self.institute_name.lower().replace(" ", "_").replace("-", "_")
