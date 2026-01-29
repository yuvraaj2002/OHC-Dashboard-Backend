import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.keyword_detection_prompt import KEYWORD_DETECTION_SYSTEM_PROMPT
from app.schema.keyword_detection_schema import KeywordDetectionOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def keyword_detection_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Analyzes the diarized transcription to detect required and prohibited phrases.
    """
    diarized_segments = state.get("call_diarization", [])
    
    # Format the diarized transcription for the prompt
    diarized_transcription = "\n".join([
        f"{seg.speaker if hasattr(seg, 'speaker') else seg.get('speaker', 'UNKNOWN')}: {seg.text if hasattr(seg, 'text') else seg.get('text', '')}" 
        for seg in diarized_segments
    ])
    
    formatted_prompt = KEYWORD_DETECTION_SYSTEM_PROMPT.format(diarized_transcription=diarized_transcription)
    
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
        text_format=KeywordDetectionOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    return {
        "keyword_detection": output_parsed,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Test case
    # uv run -m app.agents.nodes.keyword_detection_node
    sample_diarized_segments = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello, I'm calling from Optimistic Healthcare regarding your inquiry. Can I start by getting your date of birth?"},
        {"speaker": "PATIENT", "text": "Sure, it's January 1st, 1980."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Thank you. I also need to verify your insurance. Do you have your card ready?"},
        {"speaker": "PATIENT", "text": "Yes, I have it right here."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Great. Please be aware of our HIPAA acknowledgment regarding your privacy. Also, keep in mind that this visit may require prior authorization from your provider."},
        {"speaker": "PATIENT", "text": "I understand."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "And just so you know, our treatment is a guaranteed cure for your condition. You'll be 100% fine after one session."},
        {"speaker": "PATIENT", "text": "Wow, really?"},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Yes. Also, those other clinics like 'Medi-Health' are terrible and use outdated tech. We are much better."},
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
    
    print("Running Keyword & Phrase Detection Node Test...")
    result = keyword_detection_node(mock_state)
    print("\nResult:")
    print("--- Required Phrases ---")
    for res in result['keyword_detection'].required_phrases:
        print(f"[{'✓' if res.status else '✗'}] {res.phrase}: {res.context}")
    
    print("\n--- Prohibited Phrases ---")
    for res in result['keyword_detection'].prohibited_phrases:
        print(f"[{'!!' if res.status else 'OK'}] {res.phrase}: {res.context}")
    
    print(f"\nSummary: {result['keyword_detection'].overall_summary}")
    print(f"Total Cost: {result['llm_cost']}")
