from pydantic import BaseModel, Field

class QualificationCompletenessOutput(BaseModel):
    date_of_birth_collected: bool = Field(description="Whether the patient's date of birth was collected.")
    insurance_details_collected: bool = Field(description="Whether the patient's insurance details were collected.")
    symptoms_condition_collected: bool = Field(description="Whether the patient's symptoms or medical condition were discussed and collected.")
    prior_authorization_status_collected: bool = Field(description="Whether the prior authorization status was discussed or collected.")
    all_required_fields_collected: bool = Field(description="Whether all necessary fields for qualification were successfully collected.")
    reasoning: str = Field(description="Brief reasoning for the completeness check.")
