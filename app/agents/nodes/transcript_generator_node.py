import io
from openai import OpenAI
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.core.config import settings
from app.agents.tools.audio_processing_tool import AudioProcessingTool
from app.helper.openai_helper import OpenAIHelper

# Initiating the openai client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def transcription_node(state: CallQC_Analysis) -> CallQC_Analysis:
    recording_url = state["recording_url"]

    # 1. Fetch audio bytes using the tool
    audio_bytes = AudioProcessingTool.fetch_audio_bytes(recording_url)
    
    if not audio_bytes:
        raise ValueError("audio_bytes cannot be empty or failed to fetch")

    # 2. Wrap bytes in a file-like object for the transcription API
    # Proper sync: AudioProcessingTool returns bytes, we wrap in BytesIO
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"  # Filename is required for type detection

    # 3. Making inference using transcriptions API
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe-diarize",
        file=audio_file,
        response_format="diarized_json",
        chunking_strategy="auto",
        language="en",
    )

    # Getting input tokens, output tokens so that we can calculate cost
    input_tokens = transcript.usage.input_tokens
    output_tokens = transcript.usage.output_tokens
    cost = OpenAIHelper.calculate_cost(input_tokens, output_tokens, 2.0, 10.0)
    total_cost = state.get("llm_cost", 0.0) + cost

    # 4. Return the state update
    # Converting segments to dictionaries for serializability and easier access in the next node
    segments_dict = [
        {
            "speaker": seg.speaker,
            "text": seg.text,
            "start": seg.start,
            "end": seg.end
        }
        for seg in transcript.segments
    ]

    return {
        "call_transcript": {"segments": segments_dict},
        "llm_cost": total_cost,
    }

if __name__ == "__main__":
    state = {
        "recording_url": "https://www.voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav",
        "llm_cost": 0.0
    }
    result = transcription_node(state)
    print(result)
    # uv run -m app.agents.nodes.transcript_generator_node
