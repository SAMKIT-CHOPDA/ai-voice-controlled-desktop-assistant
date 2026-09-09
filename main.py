import string

from wake_word import record_command, transcribe
from assistant import ask_llm
from tts import speak


print()
print("===================================")
print("       AI VOICE ASSISTANT")
print("===================================")
print()


while True:

    # -----------------------------------------
    # LISTEN
    # -----------------------------------------

    audio = record_command()

    if audio is None:
        continue


    # -----------------------------------------
    # SPEECH → TEXT
    # -----------------------------------------

    text = transcribe(audio)

    print()
    print("You said:", text)
    print()


    if not text:
        continue


    # -----------------------------------------
    # EXIT
    # -----------------------------------------

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


    # -----------------------------------------
    # LLM
    # -----------------------------------------

    try:

        response = ask_llm(text)

    except Exception as e:

        print("LLM error:", e)

        speak(
            "Sorry, I encountered an error while processing your request."
        )

        continue


    # -----------------------------------------
    # SPEAK RESPONSE
    # -----------------------------------------

    if response:

        speak(response)