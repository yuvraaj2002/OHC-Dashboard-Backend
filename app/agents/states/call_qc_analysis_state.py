from typing import TypedDict, List, Optional, Any
from app.schema.consent_capture_schema import ConsentCaptureOutput
from app.schema.communication_quality_schema import CommunicationQualityOutput
from app.schema.keyword_detection_schema import KeywordDetectionOutput
from app.schema.sentiment_detection_schema import SentimentDetectionOutput
from app.schema.qualification_completeness_schema import QualificationCompletenessOutput
from app.schema.script_adherence_schema import ScriptAdherenceOutput
from app.schema.objection_handling_schema import ObjectionHandlingOutput
from app.schema.final_qc_report_schema import FinalQCReportOutput

class CallQC_Analysis(TypedDict):

    # Inputs
    recording_url : str

    # State variables
    call_transcript: Optional[dict]
    call_diarization: Optional[List[Any]]
    
    # Metrics
    analysis_start_time: Optional[float] # Timestamp when analysis started
    analysis_end_time: Optional[float] # Timestamp when analysis ended
    analysis_duration: Optional[float] # Total time taken for analysis in seconds

    # Analysis outputs
    consent_capture: Optional[ConsentCaptureOutput]
    communication_quality: Optional[CommunicationQualityOutput]
    keyword_detection: Optional[KeywordDetectionOutput]
    sentiment_detection: Optional[SentimentDetectionOutput]
    qualification_completeness: Optional[QualificationCompletenessOutput]
    script_adherence: Optional[ScriptAdherenceOutput]
    objection_handling: Optional[ObjectionHandlingOutput]
    
    # Final Report
    final_qc_report: Optional[FinalQCReportOutput]

    # LLM cost
    llm_cost : float