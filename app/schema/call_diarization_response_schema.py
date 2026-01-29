from pydantic import BaseModel
from typing import List, Literal

class DiarizedSegment(BaseModel):
    speaker: Literal["OHC_REPRESENTATIVE", "PATIENT"]
    text: str

class CallDiarizationOutput(BaseModel):
    segments: List[DiarizedSegment]
