import textwrap
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.agents.prompts.call_diarization_prompt import CALL_DIARIZATION_SYSTEM_PROMPT
from app.schema.call_diarization_response_schema import CallDiarizationOutput
from app.helper.openai_helper import OpenAIHelper

MODEL = "gpt-4.1-2025-04-14"
TEMPERATURE = 0.0

def call_diarization_node(state: CallQC_Analysis) -> CallQC_Analysis:
    call_transcript = state["call_transcript"]["segments"]
    raw_diarized_list = [
        f"{seg['speaker']}: {seg['text'].strip()}" for seg in call_transcript
    ]
    call_transcript_string = "\n".join(raw_diarized_list)
    formatted_prompt = textwrap.dedent(CALL_DIARIZATION_SYSTEM_PROMPT) + f"\n\nCall Transcript: {call_transcript_string}"

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
        text_format=CallDiarizationOutput,
        input_token_cost=2.0,
        output_token_cost=0.50
    )

    # Fetching the existing cost from state
    existing_cost = state.get("llm_cost", 0.0)
    total_cost = existing_cost + cost

    return {
        "call_diarization": output_parsed.segments,
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    # Sample diarized transcript (speaker A/B/C from API, to be normalized to OHC_REPRESENTATIVE / PATIENT)
    sample_segments = [
        {"speaker": "A", "text": "Hello?"},
        {"speaker": "B", "text": "Hello. Yes, hello,"},
        {"speaker": "B", "text": "Ms. Bernice. It's me,"},
        {"speaker": "B", "text": "Jessa from Optimistic Healthcare."},
        {"speaker": "B", "text": "I do apologize that the call got disconnected a while ago."},
        {"speaker": "B", "text": "So again,"},
        {"speaker": "B", "text": "please do keep your line open because you will be receiving a call from our tele,"},
        {"speaker": "B", "text": "our medical team. And please do be advised, Ms. Bernice, that they will be calling you from the area code 718, okay?"},
        {"speaker": "C", "text": "They're going to call us today."},
        {"speaker": "B", "text": "Yes, ma'am."},
        {"speaker": "C", "text": "Yeah,"},
        {"speaker": "C", "text": "okay."},
        {"speaker": "B", "text": "Thank you so much, ma'am, for taking my call."},
    ]
    state = {
        "call_transcript": {"segments": sample_segments},
        "llm_cost": 0.0,
    }
    result = call_diarization_node(state)
    print(result)