import traceback
import requests
from io import BytesIO
import logging

class AudioProcessingTool:

    def __init__(self):
        pass
    
    @staticmethod
    def fetch_audio_bytes(recording_url: str) -> bytes:
        try:
            headers = {
                "Accept": "audio/wav, audio/*, */*",
                "User-Agent": "Mozilla/5.0 (compatible; AudioFetcher/1.0)",
            }
            response = requests.get(recording_url, headers=headers, timeout=30)
            response.raise_for_status()
            logging.info(f"Successfully fetched audio bytes from {recording_url}")
            return response.content
        except Exception as e:
            logging.error(f"Error fetching audio bytes from {recording_url}: {e}\n{traceback.format_exc()}")
            raise


# if __name__ == "__main__":  
#     audio_bytes = AudioProcessingTool.fetch_audio_bytes("https://www.voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav")
#     print(audio_bytes)