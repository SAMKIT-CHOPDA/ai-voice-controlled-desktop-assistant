from __future__ import annotations

import os
import time
from statistics import mean

from dotenv import load_dotenv
from openai import OpenAI

from model_router import ModelLevel, PROFILES

load_dotenv()

PROMPTS = [
    ("FAST_QUERY", "What is RAG in AI? Answer in one or two natural sentences."),
    (
        "STANDARD_QUERY",
        "Explain how RAG works with a vector database in a concise, voice-friendly way.",
    ),
    (
        "DEEP_QUERY",
        "Compare RAG and fine-tuning. Explain the main trade-offs and when you would choose each.",
    ),
]

TEST_ORDER = [
    ModelLevel.FAST,
    ModelLevel.STANDARD,
    ModelLevel.DEEP,
]

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=60.0,
    max_retries=1,
)


def run_once(level: ModelLevel, prompt: str) -> dict:
    profile = PROFILES[level]

    start = time.perf_counter()
    first_token = None
    chunks = []

    stream = client.responses.create(
        model=profile.model,
        input=prompt,
        reasoning={"effort": profile.reasoning_effort},
        stream=True,
    )

    for event in stream:
        if event.type == "response.output_text.delta":
            if first_token is None:
                first_token = time.perf_counter() - start
            chunks.append(event.delta)

    total = time.perf_counter() - start
    text = "".join(chunks).strip()

    return {
        "level": level.value,
        "model": profile.model,
        "reasoning": profile.reasoning_effort,
        "first_token": first_token if first_token is not None else total,
        "total": total,
        "chars": len(text),
        "words": len(text.split()),
    }


def main() -> None:
    print()
    print("=" * 78)
    print("          AI VOICE ASSISTANT — MODEL LATENCY BENCHMARK")
    print("=" * 78)
    print()
    print("This benchmark does NOT modify assistant.py or JEV.")
    print("Each prompt is sent once to each model configuration.")
    print()

    results = []

    for prompt_name, prompt in PROMPTS:
        print(f"\n{'-' * 78}")
        print(f"PROMPT: {prompt_name}")
        print(f"{'-' * 78}")
        print(prompt)

        for level in TEST_ORDER:
            profile = PROFILES[level]

            print(
                f"\n[{level.value}] "
                f"{profile.model} | reasoning={profile.reasoning_effort}"
            )
            print("Running...", end="", flush=True)

            try:
                result = run_once(level, prompt)
                results.append(result)

                print(
                    f" done | first_token={result['first_token']:.3f}s"
                    f" | total={result['total']:.3f}s"
                    f" | words={result['words']}"
                )
            except Exception as exc:
                print(f" FAILED | {type(exc).__name__}: {exc}")

    if not results:
        print("\nNo successful benchmark results.")
        return

    print()
    print("=" * 78)
    print("RESULTS")
    print("=" * 78)

    print(
        f"{'Level':<10}"
        f"{'Model':<18}"
        f"{'Reason':<8}"
        f"{'First token':>14}"
        f"{'Total':>12}"
        f"{'Words':>8}"
    )
    print("-" * 78)

    for r in results:
        print(
            f"{r['level']:<10}"
            f"{r['model']:<18}"
            f"{r['reasoning']:<8}"
            f"{r['first_token']:>13.3f}s"
            f"{r['total']:>11.3f}s"
            f"{r['words']:>8}"
        )

    print()
    print("=" * 78)
    print("AVERAGES BY MODEL")
    print("=" * 78)

    for level in TEST_ORDER:
        rows = [r for r in results if r["level"] == level.value]
        if not rows:
            continue

        avg_first = mean(r["first_token"] for r in rows)
        avg_total = mean(r["total"] for r in rows)
        avg_words = mean(r["words"] for r in rows)

        model = rows[0]["model"]

        print(
            f"{level.value:<10} {model:<18}"
            f" first_token={avg_first:.3f}s"
            f" total={avg_total:.3f}s"
            f" avg_words={avg_words:.1f}"
        )

    print()
    print("BENCHMARK COMPLETE")
    print()


if __name__ == "__main__":
    main()
