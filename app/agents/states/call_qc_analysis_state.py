from typing import TypedDict, List, Optional, Any
from app.schema.consent_capture_schema import ConsentCaptureOutput
from app.schema.communication_quality_schema import CommunicationQualityOutput

class CallQC_Analysis(TypedDict):

    # Inputs
    recording_url : str

    # State variables
    call_transcript: Optional[dict]
    call_diarization: Optional[List[Any]]
    consent_capture: Optional[ConsentCaptureOutput]
    communication_quality: Optional[CommunicationQualityOutput]

    # LLM cost
    llm_cost : float