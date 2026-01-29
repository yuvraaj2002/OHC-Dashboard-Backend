import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.qualification_completeness_prompt import QUALIFICATION_COMPLETENESS_SYSTEM_PROMPT
from app.schema.qualification_completeness_schema import QualificationCompletenessOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def qualification_completeness_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Analyzes the diarized transcription to check if all qualification fields were collected.
    """
    diarized_segments = state.get("call_diarization", [])
    
    # Format the diarized transcription for the prompt
    diarized_transcription = "\n".join([
        f"{seg.speaker if hasattr(seg, 'speaker') else seg.get('speaker', 'UNKNOWN')}: {seg.text if hasattr(seg, 'text') else seg.get('text', '')}" 
        for seg in diarized_segments
    ])
    
    formatted_prompt = QUALIFICATION_COMPLETENESS_SYSTEM_PROMPT.format(diarized_transcription=diarized_transcription)
    
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
        text_format=QualificationCompletenessOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    return {
        "qualification_completeness": output_parsed,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Test case
    # uv run -m app.agents.nodes.qualification_completeness_node
    sample_diarized_segments = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello, I'm calling to qualify you for our specialized care program. Could you please confirm your date of birth?"},
        {"speaker": "PATIENT", "text": "Yes, it's June 15th, 1975."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Thank you. And which insurance provider are you currently with?"},
        {"speaker": "PATIENT", "text": "I have Blue Cross Blue Shield."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Got it. Can you describe the symptoms you've been experiencing lately?"},
        {"speaker": "PATIENT", "text": "I've been having severe lower back pain and stiffness in the mornings."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I'm sorry to hear that. Have you already received prior authorization for this type of consultation from your primary doctor?"},
        {"speaker": "PATIENT", "text": "Yes, I have high-level authorization already confirmed."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Excellent. I have everything I need to proceed with your qualification."},
    ]
    
    # Mocking the state
    from typing import NamedTuple
    class MockSegment(NamedTuple):
        speaker: str
        text: str

    mock_state = {
        "call_diarization": [MockSegment(**seg) for seg in sample_diarized_segments],
        "llm_cost": 0.0
    }
    
    print("Running Qualification Completeness Node Test...")
    result = qualification_completeness_node(mock_state)
    print("\nResult:")
    print(f"Date of Birth Collected: {result['qualification_completeness'].date_of_birth_collected}")
    print(f"Insurance Details Collected: {result['qualification_completeness'].insurance_details_collected}")
    print(f"Symptoms/Condition Collected: {result['qualification_completeness'].symptoms_condition_collected}")
    print(f"Prior Auth Status Collected: {result['qualification_completeness'].prior_authorization_status_collected}")
    print(f"All Required Fields Collected: {result['qualification_completeness'].all_required_fields_collected}")
    print(f"Reasoning: {result['qualification_completeness'].reasoning}")
    print(f"Total Cost: {result['llm_cost']}")
