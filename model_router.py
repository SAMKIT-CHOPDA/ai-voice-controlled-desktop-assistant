from __future__ import annotations

import os
import re
from dataclasses import dataclass
from enum import Enum


class ModelLevel(str, Enum):
    FAST = "FAST"
    STANDARD = "STANDARD"
    DEEP = "DEEP"


@dataclass(frozen=True)
class ModelProfile:
    level: ModelLevel
    model: str
    reasoning_effort: str


# Environment variables let us benchmark or replace models without changing code.
MODEL_FAST = os.getenv("ASSISTANT_MODEL_FAST", "gpt-5.6-luna")
MODEL_STANDARD = os.getenv("ASSISTANT_MODEL_STANDARD", "gpt-5.6-terra")
MODEL_DEEP = os.getenv("ASSISTANT_MODEL_DEEP", "gpt-5.6-sol")


PROFILES = {
    ModelLevel.FAST: ModelProfile(
        ModelLevel.FAST, MODEL_FAST, "none"
    ),
    ModelLevel.STANDARD: ModelProfile(
        ModelLevel.STANDARD, MODEL_STANDARD, "low"
    ),
    ModelLevel.DEEP: ModelProfile(
        ModelLevel.DEEP, MODEL_DEEP, "medium"
    ),
}


# Strong signals for tasks where extra reasoning is useful.
_DEEP_PATTERNS = [
    r"\banaly[sz]e\b",
    r"\banalysis\b",
    r"\bcritique\b",
    r"\bevaluate\b",
    r"\binvestigate\b",
    r"\bresearch\b",
    r"\bmethodolog(?:y|ies)\b",
    r"\bderive\b",
    r"\bproof\b",
    r"\bmathematically\b",
    r"\barchitecture\b",
    r"\bdesign a system\b",
    r"\bdesign an? (?:ai|ml|software)\b",
    r"\bcompare .+ and .+\b",
    r"\bcompare .+ with .+\b",
    r"\btrade[- ]?offs?\b",
    r"\bwhy does .+ work\b",
    r"\bhow does .+ work internally\b",
    r"\bstep[- ]by[- ]step\b",
    r"\bdebug\b",
    r"\bdebugging\b",
    r"\bcomplex\b",
    r"\bmultiple (?:steps|constraints|requirements)\b",
]

_STANDARD_PATTERNS = [
    r"\bexplain\b",
    r"\bcompare\b",
    r"\bdifference between\b",
    r"\badvantages?\b",
    r"\bdisadvantages?\b",
    r"\bpros and cons\b",
    r"\bsummar(?:ize|ise)\b",
    r"\bwrite\b",
    r"\bdraft\b",
    r"\bexample\b",
    r"\bhow do i\b",
    r"\bhow can i\b",
    r"\bhelp me\b",
]

_FAST_PATTERNS = [
    r"^what is (?:a |an |the )?.{1,80}\??$",
    r"^who is .{1,80}\??$",
    r"^where is .{1,80}\??$",
    r"^when is .{1,80}\??$",
    r"^define .{1,80}\??$",
    r"^meaning of .{1,80}\??$",
    r"^tell me about .{1,80}\??$",
    r"^what does .{1,80} mean\??$",
    r"^is .{1,100}\??$",
    r"^can .{1,100}\??$",
    r"^do .{1,100}\??$",
    r"^(hi|hello|hey|thanks|thank you|good morning|good evening)[!. ]*$",
]


def _matches(patterns: list[str], text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def classify_query(user_text: str) -> ModelLevel:
    """Choose the minimum model level likely to satisfy a GENERAL_LLM request."""
    text = re.sub(r"\s+", " ", user_text.strip())
    low = text.lower()

    if not low:
        return ModelLevel.FAST

    # Explicit complexity signals take priority.
    if _matches(_DEEP_PATTERNS, low):
        return ModelLevel.DEEP

    # Very long requests are more likely to contain multiple requirements.
    word_count = len(low.split())
    if word_count >= 45:
        return ModelLevel.DEEP

    if _matches(_STANDARD_PATTERNS, low):
        return ModelLevel.STANDARD

    if _matches(_FAST_PATTERNS, low):
        return ModelLevel.FAST

    # Short, single-intent questions are a good fit for the fast model.
    if word_count <= 12 and "?" in low:
        return ModelLevel.FAST

    return ModelLevel.STANDARD


def resolve_model_for_query(user_text: str) -> ModelProfile:
    """Return the model + reasoning configuration for a GENERAL_LLM query."""
    level = classify_query(user_text)
    return PROFILES[level]


def describe_routing(user_text: str) -> str:
    """Human-readable routing information for diagnostics/tests."""
    profile = resolve_model_for_query(user_text)
    return (
        f"[JEV L2] level={profile.level.value} "
        f"model={profile.model} reasoning={profile.reasoning_effort}"
    )
