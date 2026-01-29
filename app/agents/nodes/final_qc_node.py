import json
import time
import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.final_qc_report_prompt import FINAL_QC_SYSTEM_PROMPT
from app.schema.final_qc_report_schema import FinalQCReportOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def final_qc_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Synthesizes the results from all previous analysis nodes to generate a final QC report and score.
    Also calculates the total analysis duration.
    """
    
    # Collect data from all analysis nodes
    analysis_data = {
        "Script Adherence": state.get("script_adherence").model_dump() if state.get("script_adherence") else "N/A",
        "Qualification Completeness": state.get("qualification_completeness").model_dump() if state.get("qualification_completeness") else "N/A",
        "Consent Capture": state.get("consent_capture").model_dump() if state.get("consent_capture") else "N/A",
        "Objection Handling": state.get("objection_handling").model_dump() if state.get("objection_handling") else "N/A",
        "Communication Quality": state.get("communication_quality").model_dump() if state.get("communication_quality") else "N/A",
        "Keyword Detection": state.get("keyword_detection").model_dump() if state.get("keyword_detection") else "N/A",
        "Sentiment Detection": state.get("sentiment_detection").model_dump() if state.get("sentiment_detection") else "N/A",
    }
    
    analysis_json = json.dumps(analysis_data, indent=2)
    
    formatted_prompt = FINAL_QC_SYSTEM_PROMPT.format(analysis_data=analysis_json)
    
    helper = OpenAIHelper()
    output_parsed, cost = helper.structured_inference(
        model=MODEL,
        input=[
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": formatted_prompt}],
            }
        ],
        temperature=TEMPERATURE,
        text_format=FinalQCReportOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    # Calculate Analysis Duration
    end_time = time.time()
    start_time = state.get("analysis_start_time", end_time)
    analysis_duration = end_time - start_time
    
    return {
        "final_qc_report": output_parsed,
        "llm_cost": total_cost,
        "analysis_end_time": end_time,
        "analysis_duration": analysis_duration
    }

if __name__ == "__main__":
    # uv run -m app.agents.nodes.final_qc_node
    # Mocking a partially populated state for testing
    from app.schema.consent_capture_schema import ConsentCaptureOutput
    from app.schema.script_adherence_schema import ScriptAdherenceOutput
    
    mock_consent = ConsentCaptureOutput(
        telehealth_consent_explained=True,
        patient_verbally_agreed=True,
        hipaa_acknowledgment_mentioned=True,
        consent_documented=True,
        reasoning="All consent steps followed."
    )
    
    mock_script = ScriptAdherenceOutput(
        opening_present=True,
        closing_present=False, # Flaw
        script_followed=True,
        required_talking_points_covered=True,
        missing_points=["Closing sign-off"],
        reasoning="Good opening but forgot formal closing."
    )
    
    mock_state = {
        "script_adherence": mock_script,
        "consent_capture": mock_consent,
        "llm_cost": 0.0,
        "analysis_start_time": time.time() - 5.0 # Mock start time 5 seconds ago
        # other fields can be None/Missing for this test
    }
    
    print("Running Final QC Node Test...")
    result = final_qc_node(mock_state)
    print("\nResult:")
    print(f"Overall Score: {result['final_qc_report'].overall_score}")
    print(f"Summary: {result['final_qc_report'].summary}")
    print(f"Critical Flags: {result['final_qc_report'].critical_flags}")
    print(f"Total Cost: {result['llm_cost']}")
    print(f"Analysis Duration: {result['analysis_duration']}s")
