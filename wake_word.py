import sounddevice as sd
import numpy as np
import torch

from silero_vad import load_silero_vad, VADIterator
from faster_whisper import WhisperModel
#import string


# ============================================================
# SETTINGS
# ============================================================

SAMPLE_RATE = 16000

# Silero VAD uses 512 samples at 16 kHz
CHUNK_SIZE = 512

# How long silence should continue before we stop
SILENCE_DURATION = 1.7  # seconds


# ============================================================
# LOAD MODELS
# ============================================================

print("Loading speech detection model...")

vad_model = load_silero_vad()

print("Loading Whisper model...")

whisper_model = WhisperModel(
    "medium",
    #"large-v3-turbo",
    device="cpu",
    compute_type="int8"
)

print()
print("===================================")
print("       VOICE ASSISTANT READY")
print("===================================")
print()


# ============================================================
# RECORD ONE COMMAND
# ============================================================

def record_command():

    audio_chunks = []

    speech_started = False
    silence_samples = 0

    # Create a fresh streaming VAD
    vad = VADIterator(
        vad_model,
        sampling_rate=SAMPLE_RATE,
        min_silence_duration_ms=1700
    )

    print("Listening...")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=CHUNK_SIZE
    ) as stream:

        while True:

            # Get 512 samples from microphone
            audio, overflowed = stream.read(CHUNK_SIZE)

            # Convert to a 1-D PyTorch tensor
            audio_tensor = torch.from_numpy(
                audio[:, 0].copy()
            )

            # Feed this chunk to streaming VAD
            result = vad(
                audio_tensor,
                return_seconds=False
            )

            # ------------------------------------------------
            # SPEECH STARTED
            # ------------------------------------------------

            if result is not None and "start" in result:

                speech_started = True

                print("Speech detected...")

                # Start saving audio
                audio_chunks.append(audio.copy())

            # ------------------------------------------------
            # SPEECH CONTINUING
            # ------------------------------------------------

            elif speech_started:

                audio_chunks.append(audio.copy())

                # Check whether VAD says speech ended
                if result is not None and "end" in result:

                    print("Speech ended.")

                    # Save the final chunk
                    break

    # Reset VAD state
    vad.reset_states()

    if not audio_chunks:
        return None

    # Combine all chunks into one recording
    complete_audio = np.concatenate(
        audio_chunks,
        axis=0
    )

    return complete_audio


# ============================================================
# TRANSCRIBE
# ============================================================

def transcribe(audio):

    print("Transcribing...")

    audio = audio.flatten()

    segments, info = whisper_model.transcribe(
        audio,
        language="en",
        vad_filter=True
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()

'''
# ============================================================
# MAIN LOOP
# ============================================================

while True:

    audio = record_command()

    if audio is None:
        continue

    text = transcribe(audio)

    print()
    print("-----------------------------------")
    print("You said:", text)
    print("-----------------------------------")
    print()

    clean_text = text.lower().strip().translate(
    str.maketrans("", "", string.punctuation)
)

    if clean_text in ["exit", "quit", "stop assistant"]:

        print("Assistant stopped.")

        break
'''