import os
import time
import queue
import threading

import sounddevice as sd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"
SAMPLE_RATE = 24000
CHANNELS = 1
DTYPE = "int16"

_audio_queue = queue.Queue()
_worker_thread = None
_worker_lock = threading.Lock()


def _audio_worker():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=30.0,
        max_retries=1,
    )

    output_stream = sd.RawOutputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        blocksize=0,
    )
    output_stream.start()

    try:
        while True:
            text = _audio_queue.get()

            if text is None:
                _audio_queue.task_done()
                break

            try:
                start = time.perf_counter()
                print(f"[TTS] chunk_start={text[:60]!r}")
                first_audio = None

                with client.audio.speech.with_streaming_response.create(
                    model=TTS_MODEL,
                    voice=TTS_VOICE,
                    input=text,
                    response_format="pcm",
                ) as response:
                    for chunk in response.iter_bytes(chunk_size=4096):
                        if not chunk:
                            continue

                        if first_audio is None:
                            first_audio = time.perf_counter() - start
                            print(f"[TTS] first_audio={first_audio:.3f}s")

                        output_stream.write(chunk)

                print(
                    f"[TTS] chunk_complete="
                    f"{time.perf_counter() - start:.3f}s"
                )

            except Exception as exc:
                print(
                    f"[TTS] chunk error: "
                    f"{type(exc).__name__}: {exc}"
                )

            finally:
                _audio_queue.task_done()

    finally:
        output_stream.stop()
        output_stream.close()
        try:
            client.close()
        except Exception:
            pass


def _ensure_worker():
    global _worker_thread

    with _worker_lock:
        if _worker_thread is None or not _worker_thread.is_alive():
            _worker_thread = threading.Thread(
                target=_audio_worker,
                daemon=True,
            )
            _worker_thread.start()


def queue_text(text):
    if not text or not text.strip():
        return

    _ensure_worker()
    _audio_queue.put(text.strip())


def wait_for_audio():
    _audio_queue.join()


def speak(text):
    if not text or not text.strip():
        return

    print("Assistant:", text)
    queue_text(text)
    wait_for_audio()


def speak_stream_chunk(text):
    queue_text(text)
