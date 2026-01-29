from typing import TypedDict, List, Optional, Any
from app.schema.consent_capture_schema import ConsentCaptureOutput
from app.schema.communication_quality_schema import CommunicationQualityOutput
from app.schema.keyword_detection_schema import KeywordDetectionOutput
from app.schema.sentiment_detection_schema import SentimentDetectionOutput
from app.schema.qualification_completeness_schema import QualificationCompletenessOutput

class CallQC_Analysis(TypedDict):

    # Inputs
    recording_url : str

    # State variables
    call_transcript: Optional[dict]
    call_diarization: Optional[List[Any]]
    consent_capture: Optional[ConsentCaptureOutput]
    communication_quality: Optional[CommunicationQualityOutput]
    keyword_detection: Optional[KeywordDetectionOutput]
    sentiment_detection: Optional[SentimentDetectionOutput]
    qualification_completeness: Optional[QualificationCompletenessOutput]

    # LLM cost
    llm_cost : float