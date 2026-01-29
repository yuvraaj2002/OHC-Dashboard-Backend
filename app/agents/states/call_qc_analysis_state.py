from typing import TypedDict, List, Optional, Any

class CallQC_Analysis(TypedDict):

    # Inputs
    recording_url : str

    # State variables
    call_transcript: Optional[dict]
    call_diarization: Optional[List[Any]]

    # LLM cost
    llm_cost : float