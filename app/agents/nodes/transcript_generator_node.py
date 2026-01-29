import io
import time
from openai import OpenAI
from app.agents.states.call_qc_analysis_state import CallQC_Analysis
from app.core.config import settings
from app.agents.tools.audio_processing_tool import AudioProcessingTool
from app.helper.openai_helper import OpenAIHelper

# Initiating the openai client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def transcription_node(state: CallQC_Analysis) -> CallQC_Analysis:
    recording_url = state["recording_url"]
    
    # Capture start time if not already set
    start_time = state.get("analysis_start_time") or time.time()

    # 1. Fetch audio bytes using the tool
    audio_bytes = AudioProcessingTool.fetch_audio_bytes(recording_url)
    
    if not audio_bytes:
        raise ValueError("audio_bytes cannot be empty or failed to fetch")

    # 2. Wrap bytes in a file-like object for the transcription API
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"  # Filename is required for type detection

    # 3. Making inference using the specialized transcription/diarization model
    # Per user request, using gpt-4o-transcribe-diarize with token-based pricing
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe-diarize",
        file=audio_file,
        response_format="diarized_json",
        chunking_strategy="auto",
        language="en",
    )

    # 4. Calculate Token-based Cost
    # This model uses tokens for pricing as it is an LLM-based diarizer
    input_tokens = getattr(transcript.usage, "input_tokens", 0)
    output_tokens = getattr(transcript.usage, "output_tokens", 0)
    
    # Pricing: $2.00 / 1M Input, $10.00 / 1M Output (standard gpt-4o audio rates)
    cost = OpenAIHelper.calculate_cost(input_tokens, output_tokens, 2.0, 10.0)
    total_cost = state.get("llm_cost", 0.0) + cost

    # 5. Return the state update
    # Converting segments to dictionaries
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
        "analysis_start_time": start_time
    }

if __name__ == "__main__":
    state = {
        "recording_url": "https://www.voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav",
        "llm_cost": 0.0
    }
    result = transcription_node(state)
    print(result)
    # uv run -m app.agents.nodes.transcript_generator_node
