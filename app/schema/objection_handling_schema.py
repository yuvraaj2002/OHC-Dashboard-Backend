from pydantic import BaseModel, Field
from typing import List, Optional

class ObjectionHandlingResult(BaseModel):
    objection_type: str = Field(description="The type of objection (e.g., Pricing, Insurance, Competitor).")
    patient_statement: str = Field(description="The specific concern or objection raised by the patient.")
    agent_response: str = Field(description="How the agent addressed the objection.")
    handled_well: bool = Field(description="Whether the agent handled the objection professionally and effectively.")
    outcome: str = Field(description="The final outcome of the objection (e.g., Resolved, Escalated, Pending).")

class ObjectionHandlingOutput(BaseModel):
    objections_found: bool = Field(description="Whether any objections were raised during the call.")
    objection_details: List[ObjectionHandlingResult] = Field(description="List of specific objections and how they were handled.")
    overall_handling_score: float = Field(description="A score from 0-100 reflecting the agent's effectiveness in handling objections.")
    reasoning: str = Field(description="Brief reasoning for the overall objection handling evaluation.")
