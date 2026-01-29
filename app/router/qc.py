from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.graph.call_qc_graph import call_qc_graph

router = APIRouter(prefix="/qc", tags=["qc"])

class QCAnalysisRequest(BaseModel):
    recording_url: str

class QCAnalysisResponse(BaseModel):
    success: bool
    analysis_duration: float
    llm_cost: float
    overall_score: int
    summary: str
    key_strengths: list
    areas_for_improvement: list
    critical_flags: list
    reasoning: str
    # Individual analysis results
    script_adherence: dict | None
    qualification_completeness: dict | None
    consent_capture: dict | None
    objection_handling: dict | None
    communication_quality: dict | None
    keyword_detection: dict | None
    sentiment_detection: dict | None

@router.post("/analyze", response_model=QCAnalysisResponse)
async def analyze_call(request: QCAnalysisRequest):
    """
    Run the full QC analysis pipeline on a call recording.
    """
    try:
        initial_state = {
            "recording_url": request.recording_url,
            "llm_cost": 0.0
        }
        
        final_state = call_qc_graph.invoke(initial_state)
        
        report = final_state.get('final_qc_report')
        if not report:
            raise HTTPException(status_code=500, detail="Final QC Report was not generated.")
        
        return QCAnalysisResponse(
            success=True,
            analysis_duration=final_state.get('analysis_duration') or 0.0,
            llm_cost=final_state.get('llm_cost') or 0.0,
            overall_score=report.overall_score,
            summary=report.summary,
            key_strengths=report.key_strengths,
            areas_for_improvement=report.areas_for_improvement,
            critical_flags=report.critical_flags,
            reasoning=report.reasoning,
            script_adherence=final_state.get('script_adherence').model_dump() if final_state.get('script_adherence') else None,
            qualification_completeness=final_state.get('qualification_completeness').model_dump() if final_state.get('qualification_completeness') else None,
            consent_capture=final_state.get('consent_capture').model_dump() if final_state.get('consent_capture') else None,
            objection_handling=final_state.get('objection_handling').model_dump() if final_state.get('objection_handling') else None,
            communication_quality=final_state.get('communication_quality').model_dump() if final_state.get('communication_quality') else None,
            keyword_detection=final_state.get('keyword_detection').model_dump() if final_state.get('keyword_detection') else None,
            sentiment_detection=final_state.get('sentiment_detection').model_dump() if final_state.get('sentiment_detection') else None,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
