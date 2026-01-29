from pydantic import BaseModel, Field
from typing import List

class ScriptAdherenceOutput(BaseModel):
    opening_present: bool = Field(description="Whether the required opening/introduction was present in the call.")
    closing_present: bool = Field(description="Whether the required closing/sign-off was present in the call.")
    script_followed: bool = Field(description="Overall evaluation of whether the agent followed the prescribed script structure.")
    required_talking_points_covered: bool = Field(description="Whether all predefined talking points were covered during the conversation.")
    missing_points: List[str] = Field(description="List of specific talking points or script elements that were missing.")
    reasoning: str = Field(description="Brief reasoning for the script adherence evaluation.")
