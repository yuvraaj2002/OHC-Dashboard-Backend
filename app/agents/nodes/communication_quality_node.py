import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.communication_quality_prompt import COMMUNICATION_QUALITY_SYSTEM_PROMPT
from app.schema.communication_quality_schema import CommunicationQualityOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def communication_quality_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Analyzes the diarized transcription to evaluate communication quality.
    """
    diarized_segments = state.get("call_diarization", [])
    
    # Format the diarized transcription for the prompt
    # Each segment in call_diarization is expected to have 'speaker' and 'text'
    diarized_transcription = "\n".join([
        f"{seg.speaker if hasattr(seg, 'speaker') else seg.get('speaker', 'UNKNOWN')}: {seg.text if hasattr(seg, 'text') else seg.get('text', '')}" 
        for seg in diarized_segments
    ])
    
    formatted_prompt = COMMUNICATION_QUALITY_SYSTEM_PROMPT.format(diarized_transcription=diarized_transcription)
    
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
        text_format=CommunicationQualityOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    return {
        "communication_quality": output_parsed,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Test case
    # uv run -m app.agents.nodes.communication_quality_node
    sample_diarized_segments = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello Mr. Johnson, I'm sorry to hear that you haven't been feeling well lately."},
        {"speaker": "PATIENT", "text": "Yeah, my back has been killing me for the last week."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I can certainly understand how frustrating and painful that must be. We'll do our best to get you scheduled with a specialist quickly."},
        {"speaker": "PATIENT", "text": "Do you think I need surgery?"},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I'm not a doctor, so I can't provide a diagnosis or recommend a specific treatment like surgery. However, the specialist will be able to perform a full evaluation and discuss your options."},
        {"speaker": "PATIENT", "text": "Will this specialist be able to fix me for sure?"},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Our specialists are highly experienced, but I cannot guarantee a specific outcome. What I can promise is that they will provide you with the highest quality of care and work with you on a personalized treatment plan."},
        {"speaker": "PATIENT", "text": "Okay, that sounds fair."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Let's go ahead and find a time that works for you. Are you available this Thursday?"},
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
    
    print("Running Communication Quality Node Test...")
    result = communication_quality_node(mock_state)
    print("\nResult:")
    print(f"Tone Polite & Professional: {result['communication_quality'].tone_polite_professional}")
    print(f"Empathy Shown: {result['communication_quality'].empathy_shown}")
    print(f"Clarity of Communication: {result['communication_quality'].clarity_of_communication}")
    print(f"No Illegal Medical Advice: {result['communication_quality'].no_illegal_medical_advice}")
    print(f"No Guarantees/Promises: {result['communication_quality'].no_guarantees_promises}")
    print(f"Reasoning: {result['communication_quality'].reasoning}")
    print(f"Total Cost: {result['llm_cost']}")
