from pydantic import BaseModel, Field

class ConsentCaptureOutput(BaseModel):
    telehealth_consent_explained: bool = Field(description="Whether the agent explained telehealth consent.")
    patient_verbally_agreed: bool = Field(description="Whether the patient verbally agreed to the consent.")
    hipaa_acknowledgment_mentioned: bool = Field(description="Whether HIPAA acknowledgment was mentioned.")
    consent_documented: bool = Field(description="Whether the consent was documented properly during the call.")
    reasoning: str = Field(description="Brief reasoning for the binary outcomes.")
