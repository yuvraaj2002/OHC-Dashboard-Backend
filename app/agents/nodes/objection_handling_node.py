import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.objection_handling_prompt import OBJECTION_HANDLING_SYSTEM_PROMPT
from app.schema.objection_handling_schema import ObjectionHandlingOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def objection_handling_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Analyzes the diarized transcription to evaluate objection handling.
    """
    diarized_segments = state.get("call_diarization", [])
    
    # Format the diarized transcription for the prompt
    diarized_transcription = "\n".join([
        f"{seg.speaker if hasattr(seg, 'speaker') else seg.get('speaker', 'UNKNOWN')}: {seg.text if hasattr(seg, 'text') else seg.get('text', '')}" 
        for seg in diarized_segments
    ])
    
    formatted_prompt = OBJECTION_HANDLING_SYSTEM_PROMPT.format(diarized_transcription=diarized_transcription)
    
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
        text_format=ObjectionHandlingOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    return {
        "objection_handling": output_parsed,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Test case
    # uv run -m app.agents.nodes.objection_handling_node
    sample_diarized_segments = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello, I'm calling from Optimistic Healthcare. Our program costs $150 per month."},
        {"speaker": "PATIENT", "text": "That's quite expensive. I wasn't expecting it to be that much."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I understand the concern about pricing. However, this includes 24/7 access to our medical team and all your medication deliveries. Compared to others like 'Medi-Fast', we offer a more comprehensive service for a similar price point."},
        {"speaker": "PATIENT", "text": "What about my insurance? Does it cover any of this?"},
        {"speaker": "OHC_REPRESENTATIVE", "text": "We do work with several providers. I can check your specific plan right now to see if we can lower that out-of-pocket cost for you."},
        {"speaker": "PATIENT", "text": "Okay, that's better. Please check."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I've checked and your plan covers 50%, so it would only be $75 for you."},
        {"speaker": "PATIENT", "text": "Oh, that's much more reasonable. I'm happy with that."},
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
    
    print("Running Objection Handling Node Test...")
    result = objection_handling_node(mock_state)
    print("\nResult:")
    print(f"Objections Found: {result['objection_handling'].objections_found}")
    if result['objection_handling'].objections_found:
        for obj in result['objection_handling'].objection_details:
            print(f"---\nType: {obj.objection_type}")
            print(f"Patient: {obj.patient_statement}")
            print(f"Agent: {obj.agent_response}")
            print(f"Handled Well: {obj.handled_well}")
            print(f"Outcome: {obj.outcome}")
    
    print(f"\nOverall Score: {result['objection_handling'].overall_handling_score}")
    print(f"Reasoning: {result['objection_handling'].reasoning}")
    print(f"Total Cost: {result['llm_cost']}")
