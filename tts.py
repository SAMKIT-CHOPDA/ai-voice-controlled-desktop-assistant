from pathlib import Path

from openai import OpenAI
from playsound3 import playsound


client = OpenAI()

AUDIO_FILE = Path("assistant_response.mp3")


def speak(text):

    print("Assistant:", text)

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as response:

        response.stream_to_file(AUDIO_FILE)

    playsound(str(AUDIO_FILE))