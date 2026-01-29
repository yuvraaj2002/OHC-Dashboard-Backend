import os
import io
from openai import OpenAI
from pydub import AudioSegment
from app.core.config import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_conversation_audio(segments, output_file="test_call.wav"):
    """
    Generates a multi-speaker audio file using OpenAI's TTS.
    
    Voices:
    - OHC_REPRESENTATIVE: 'alloy' (Professional/Neutral)
    - PATIENT: 'nova' (Warm/Relatable)
    """
    combined_audio = AudioSegment.empty()
    
    print(f"Generating audio for {len(segments)} segments...")
    
    for i, segment in enumerate(segments):
        speaker = segment["speaker"]
        text = segment["text"]
        
        # Select voice based on speaker
        voice = "alloy" if speaker == "OHC_REPRESENTATIVE" else "nova"
        
        print(f"  [{i+1}/{len(segments)}] Generating {speaker} speech...")
        
        # Call OpenAI TTS API
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Read the raw MP3 data into pydub
        audio_data = io.BytesIO(response.content)
        segment_audio = AudioSegment.from_file(audio_data, format="mp3")
        
        # Add a small pause (silence) between segments
        silence = AudioSegment.silent(duration=500) # 500ms
        
        combined_audio += segment_audio + silence

    # Export as WAV
    print(f"Exporting combined audio to {output_file}...")
    combined_audio.export(output_file, format="wav")
    print("Done!")

if __name__ == "__main__":
    # This "Perfect Transcript" covers all the agents we built:
    # 1. Opening + Scripts
    # 2. Consent + HIPAA
    # 3. Qualification (DOB, Insurance, Symptoms)
    # 4. Objection Handling (Pricing)
    # 5. Tone + Empathy
    # 6. Closing
    
    test_transcript = [
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hello, this is Jessa from Optimistic Healthcare. Am I speaking with Mr. Robert?"},
        {"speaker": "PATIENT", "text": "Yes, this is Robert."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Hi Robert, I'm calling to follow up on your inquiry. Before we start, I need to explain that this is a telehealth consultation. Do you verbally agree to proceed with this remote visit?"},
        {"speaker": "PATIENT", "text": "Yes, I agree to that."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Great. Also, please note that we follow all HIPAA guidelines to keep your data protected. Can you please confirm your date of birth?"},
        {"speaker": "PATIENT", "text": "It is July 12th, 1985."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Thank you. And which insurance do you use?"},
        {"speaker": "PATIENT", "text": "I have Aetna."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "Perfect. Now, can you tell me a bit about the symptoms you are feeling?"},
        {"speaker": "PATIENT", "text": "I've had a really bad cough and headache for three days. It's quite painful actually."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I'm so sorry to hear you're in pain, Robert. That sounds very uncomfortable. I'll make sure we get a specialist to look at this today."},
        {"speaker": "PATIENT", "text": "How much will this cost? I'm worried it's too expensive."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "I understand the concern. Our initial consult is usually $100, but with Aetna, it might be fully covered. I'll verify that for you right now so you don't have to worry."},
        {"speaker": "PATIENT", "text": "Okay, that would be a relief. Thank you."},
        {"speaker": "OHC_REPRESENTATIVE", "text": "You're very welcome. I am documenting your consent and prior authorization status in our system. We are all set. Thank you for choosing OHC, and have a better day!"},
        {"speaker": "PATIENT", "text": "Thank you, goodbye."}
    ]

    # Requirements:
    # pip install pydub openai
    # Also requires 'ffmpeg' installed on your system
    
    print("Pre-requisite check: Ensure you have 'pydub' installed and 'ffmpeg' on your PATH.")
    generate_conversation_audio(test_transcript, "perfect_test_call.wav")
