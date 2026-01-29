from pydantic import BaseModel, Field
from typing import List

class KeywordDetectionResult(BaseModel):
    phrase: str = Field(description="The phrase that was detected or is being checked.")
    status: bool = Field(description="True if found (for required) or True if detected (for prohibited).")
    context: str = Field(description="The snippet or context from the transcript where the phrase or violation was found, or an explanation if missing.")

class KeywordDetectionOutput(BaseModel):
    required_phrases: List[KeywordDetectionResult] = Field(description="Evaluation of required phrases.")
    prohibited_phrases: List[KeywordDetectionResult] = Field(description="Evaluation of prohibited phrases or categories.")
    overall_summary: str = Field(description="Brief summary of the keyword and phrase detection analysis.")
