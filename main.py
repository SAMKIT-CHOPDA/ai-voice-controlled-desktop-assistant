import string
import time

from wake_word import record_command, transcribe
from assistant import ask_llm
from tts import speak


print()
print("===================================")
print("       AI VOICE ASSISTANT")
print("===================================")
print()


while True:

    audio = record_command()

    if audio is None:
        continue

    text = transcribe(audio)

    print()
    print("You said:", text)
    print()

    request_start = time.perf_counter()

    if not text:
        continue

    clean_text = text.lower().strip().translate(
        str.maketrans("", "", string.punctuation)
    )

    if clean_text in [
        "exit",
        "quit",
        "stop assistant"
    ]:

        speak("Goodbye.")
        break

    try:
        response = ask_llm(text)

    except Exception as e:

        print("LLM error:", e)

        speak(
            "Sorry, I encountered an error while processing your request."
        )

        continue

    if response:
        speak(response)

    print(
        f"[TOTAL] request_to_audio_complete="
        f"{time.perf_counter() - request_start:.3f}s"
    )