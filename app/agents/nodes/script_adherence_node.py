import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.script_adherence_prompt import SCRIPT_ADHERENCE_SYSTEM_PROMPT
from app.schema.script_adherence_schema import ScriptAdherenceOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def script_adherence_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Analyzes the diarized transcription to evaluate script adherence.
    """
    diarized_segments = state.get("call_diarization", [])
    
    # Format the diarized transcription for the prompt
    diarized_transcription = "\n".join([
        f"{seg.speaker if hasattr(seg, 'speaker') else seg.get('speaker', 'UNKNOWN')}: {seg.text if hasattr(seg, 'text') else seg.get('text', '')}" 
        for seg in diarized_segments
    ])
    
    formatted_prompt = SCRIPT_ADHERENCE_SYSTEM_PROMPT.format(diarized_transcription=diarized_transcription)
    
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
        text_format=ScriptAdherenceOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    return {
        "script_adherence": output_parsed,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Test case
    # uv run -m app.agents.nodes.script_adherence_node
    sample_diarized_segments = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello, this is Sarah from Optimistic Healthcare. How are you today?"},
        {"speaker": "PATIENT", "text": "I'm fine, thanks."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I'm calling to discuss your recent inquiry about our physical therapy services. I'd like to go over some details and next steps with you."},
        {"speaker": "PATIENT", "text": "Okay, sure."},
        # Missing some talking points in this mock to test missing_points
        {"speaker": "OHC_REPRESENTATIVE", "text": "Great. That covers what I needed for now. Thank you for your time, and have a wonderful day!"},
        {"speaker": "PATIENT", "text": "You too, bye."},
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
    
    print("Running Script Adherence Node Test...")
    result = script_adherence_node(mock_state)
    print("\nResult:")
    print(f"Opening Present: {result['script_adherence'].opening_present}")
    print(f"Closing Present: {result['script_adherence'].closing_present}")
    print(f"Script Followed: {result['script_adherence'].script_followed}")
    print(f"Required Talking Points Covered: {result['script_adherence'].required_talking_points_covered}")
    print(f"Missing Points: {result['script_adherence'].missing_points}")
    print(f"Reasoning: {result['script_adherence'].reasoning}")
    print(f"Total Cost: {result['llm_cost']}")
