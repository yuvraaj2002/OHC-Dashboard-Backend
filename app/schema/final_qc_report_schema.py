from pydantic import BaseModel, Field
from typing import List

class FinalQCReportOutput(BaseModel):
    overall_score: int = Field(description="The final Quality Control score for the call (0-100).")
    summary: str = Field(description="A comprehensive executive summary of the call analysis.")
    key_strengths: List[str] = Field(description="List of key strengths demonstrated by the agent.")
    areas_for_improvement: List[str] = Field(description="List of areas where the agent needs improvement.")
    critical_flags: List[str] = Field(description="List of any critical compliance or quality flags raised.")
    reasoning: str = Field(description="Detailed reasoning for the overall score calculation.")
