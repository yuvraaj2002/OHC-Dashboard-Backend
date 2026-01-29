from pydantic import BaseModel, Field

class CommunicationQualityOutput(BaseModel):
    tone_polite_professional: bool = Field(description="Whether the agent's tone was polite and professional.")
    empathy_shown: bool = Field(description="Whether the agent demonstrated empathy towards the patient.")
    clarity_of_communication: bool = Field(description="Whether the agent's communication was clear and easy to understand.")
    no_illegal_medical_advice: bool = Field(description="Whether the agent avoided giving illegal medical advice.")
    no_guarantees_promises: bool = Field(description="Whether the agent avoided making unauthorized guarantees or promises.")
    reasoning: str = Field(description="Brief reasoning for the outcomes based on the transcription.")
