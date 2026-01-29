import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.sentiment_detection_prompt import SENTIMENT_DETECTION_SYSTEM_PROMPT
from app.schema.sentiment_detection_schema import SentimentDetectionOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def sentiment_detection_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Analyzes the diarized transcription to detect sentiment (frustration, confusion) and escalation risk.
    """
    diarized_segments = state.get("call_diarization", [])
    
    # Format the diarized transcription for the prompt
    diarized_transcription = "\n".join([
        f"{seg.speaker if hasattr(seg, 'speaker') else seg.get('speaker', 'UNKNOWN')}: {seg.text if hasattr(seg, 'text') else seg.get('text', '')}" 
        for seg in diarized_segments
    ])
    
    formatted_prompt = SENTIMENT_DETECTION_SYSTEM_PROMPT.format(diarized_transcription=diarized_transcription)
    
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
        text_format=SentimentDetectionOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    return {
        "sentiment_detection": output_parsed,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Test case
    # uv run -m app.agents.nodes.sentiment_detection_node
    sample_diarized_segments = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello, I'm calling from Optimistic Healthcare regarding your medication delivery."},
        {"speaker": "PATIENT", "text": "Wait, what? I thought it was coming yesterday. I've been waiting all day!"},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I apologize for the delay. There was an issue with the courier."},
        {"speaker": "PATIENT", "text": "I don't understand. Why didn't anyone call me? This is very frustrating. I need my medicine!"},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I understand your frustration. I am looking into it now."},
        {"speaker": "PATIENT", "text": "If this isn't resolved today, I want to talk to your supervisor. I'm thinking of switching to another provider if this keeps happening."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I will do everything I can to get this sorted out immediately..."},
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
    
    print("Running Sentiment Detection Node Test...")
    result = sentiment_detection_node(mock_state)
    print("\nResult:")
    print(f"Frustration Detected: {result['sentiment_detection'].frustration_detected}")
    print(f"Confusion Detected: {result['sentiment_detection'].confusion_detected}")
    print(f"Escalation Risk: {result['sentiment_detection'].escalation_risk}")
    print(f"Overall Sentiment: {result['sentiment_detection'].overall_sentiment}")
    print(f"Reasoning: {result['sentiment_detection'].reasoning}")
    print(f"Total Cost: {result['llm_cost']}")
