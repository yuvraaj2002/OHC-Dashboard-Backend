import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.consent_capture_prompt import CONSENT_CAPTURE_SYSTEM_PROMPT
from app.schema.consent_capture_schema import ConsentCaptureOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def consent_capture_node(state: CallQC_Analysis) -> CallQC_Analysis:
    """
    Analyzes the diarized transcription to detect compliance-critical consent capture steps.
    """
    diarized_segments = state.get("call_diarization", [])
    
    # Format the diarized transcription for the prompt
    # Each segment in call_diarization is expected to have 'speaker' and 'text'
    diarized_transcription = "\n".join([f"{seg.speaker if hasattr(seg, 'speaker') else seg.get('speaker', 'UNKNOWN')}: {seg.text if hasattr(seg, 'text') else seg.get('text', '')}" for seg in diarized_segments])
    
    formatted_prompt = CONSENT_CAPTURE_SYSTEM_PROMPT.format(diarized_transcription=diarized_transcription)
    
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
        text_format=ConsentCaptureOutput,
        input_token_cost=0.15,
        output_token_cost=0.60
    )
    
    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost
    
    return {
        "consent_capture": output_parsed,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Test case
    # uv run -m app.agents.nodes.consent_capture_node
    sample_diarized_segments = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello Ms. Smith, this is John from Optimistic Healthcare. How are you today?"},
        {"speaker": "PATIENT", "text": "I'm doing well, thank you."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Great. Before we begin, I need to explain that this is a telehealth consultation, which means it will be conducted remotely via video or phone. Do you understand and agree to proceed with this telehealth visit?"},
        {"speaker": "PATIENT", "text": "Yes, I understand and I agree."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Perfect. Also, I want to mention that we follow all HIPAA guidelines to ensure your medical information is private and protected. You've received our HIPAA acknowledgment form, correct?"},
        {"speaker": "PATIENT", "text": "Yes, I have it right here."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Excellent. I am documenting your consent and the HIPAA acknowledgment in our system right now."},
        {"speaker": "PATIENT", "text": "Thank you."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Now, let's verify your date of birth..."},
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
    
    print("Running Consent Capture Node Test...")
    result = consent_capture_node(mock_state)
    print("\nResult:")
    print(f"Telehealth Consent Explained: {result['consent_capture'].telehealth_consent_explained}")
    print(f"Patient Verbally Agreed: {result['consent_capture'].patient_verbally_agreed}")
    print(f"HIPAA Acknowledgment Mentioned: {result['consent_capture'].hipaa_acknowledgment_mentioned}")
    print(f"Consent Documented: {result['consent_capture'].consent_documented}")
    print(f"Reasoning: {result['consent_capture'].reasoning}")
    print(f"Total Cost: {result['llm_cost']}")
