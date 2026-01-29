from pydantic import BaseModel, Field

class SentimentDetectionOutput(BaseModel):
    frustration_detected: bool = Field(description="Whether frustration was detected in the patient's or agent's tone/language.")
    confusion_detected: bool = Field(description="Whether the patient appeared confused or expressed lack of understanding.")
    escalation_risk: bool = Field(description="Whether the call shows signs of high risk for escalation (e.g., threat to cancel, supervisor request, extreme dissatisfaction).")
    overall_sentiment: str = Field(description="A brief description of the overall sentiment of the call (e.g., Positive, Neutral, Negative, Mixed).")
    reasoning: str = Field(description="Brief reasoning for the detected sentiments and escalation risk.")
