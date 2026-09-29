"""TypeSafe Jev fast routing layer for the desktop voice assistant.

Jev is used only for structured routing. It does not generate the assistant's
spoken response. High-confidence routes are executed locally; everything else
falls through to the existing OpenAI agent.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from urllib.parse import quote_plus

import requests
from dotenv import load_dotenv

from tools import (
    open_application,
    open_website,
    search_web,
    play_youtube,
    get_current_time,
    get_current_date,
    battery_status,
    take_screenshot,
)
load_dotenv()

JEV_URL = os.getenv("TYPESAFE_BASE_URL", "https://api.typesafe.ai") + "/v1/systemone"
JEV_MODEL = os.getenv("TYPESAFE_DEFAULT_MODEL", "jev-latest")
JEV_API_KEY = os.getenv("TYPESAFE_API_KEY", "").strip()
JEV_TIMEOUT = float(os.getenv("JEV_TIMEOUT_SECONDS", "2.5"))
JEV_CONFIDENCE_THRESHOLD = float(os.getenv("JEV_CONFIDENCE_THRESHOLD", "0.70"))

ROUTES = {
    "SYSTEM_TIME": "Current time or clock request.",
    "SYSTEM_DATE": "Current date request.",
    "SYSTEM_BATTERY": "Battery percentage or battery status request.",
    "SCREENSHOT": "Take or capture a screenshot of the computer screen.",
    "OPEN_APPLICATION": "Open, launch, or start a desktop application such as Chrome, Edge, Notepad, Calculator, Paint, or File Explorer.",
    "OPEN_WEBSITE": "Open or go to a website without searching for something.",
    "GOOGLE_SEARCH": "Search Google for a user-provided query.",
    "YOUTUBE_SEARCH": "Search YouTube for a user-provided query.",
    "YOUTUBE_PLAY": "Play a YouTube video matching the user request, including general play requests and selected results such as the first, second, or third video.",
    "GENERAL_LLM": "A question, explanation, research request, complex instruction, or anything that does not fit the direct desktop actions above.",
}

APP_ALIASES = {
    "chrome": "Chrome",
    "google chrome": "Chrome",
    "edge": "Edge",
    "microsoft edge": "Edge",
    "notepad": "Notepad",
    "calculator": "Calculator",
    "calc": "Calculator",
    "paint": "Paint",
    "file explorer": "File Explorer",
    "explorer": "File Explorer",
}


@dataclass
class JevDecision:
    route: str
    confidence: float
    latency: float
    source: str = "jev"


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _strip_terminal_punctuation(text: str) -> str:
    """Normalize harmless sentence-ending punctuation from voice commands.

    This is intentionally generic: punctuation at the end of a spoken command
    should not change its meaning, while meaningful internal punctuation such
    as the apostrophe in "Jojo's" is preserved.
    """
    value = text.strip()
    while value and value[-1] in ".,!?;:\"'\u201d\u2019)]}\u00bb":
        value = value[:-1].rstrip()
    return value

def _local_route(text: str) -> JevDecision:
    """Safe fallback when Jev is unavailable."""
    low = _strip_terminal_punctuation(text).lower()
    start = time.perf_counter()
    if low in {"what time is it", "tell me the time", "time", "current time"}: route = "SYSTEM_TIME"
    elif low in {"what is today's date", "what's today's date", "what is the date", "what's the date", "today's date"}: route = "SYSTEM_DATE"
    elif low in {"what is my battery percentage", "what's my battery percentage", "battery percentage", "battery status", "check my battery"}: route = "SYSTEM_BATTERY"
    elif low in {"take a screenshot", "take screenshot", "capture my screen", "capture the screen", "screenshot"}: route = "SCREENSHOT"
    elif re.fullmatch(r"(?:open|launch|start)\s+(.+)", low):
        requested = re.fullmatch(r"(?:open|launch|start)\s+(.+)", low).group(1).strip()
        route = "OPEN_APPLICATION" if requested in APP_ALIASES else "OPEN_WEBSITE" if "." in requested else "GENERAL_LLM"
    elif low in {"open youtube", "launch youtube", "go to youtube", "open google", "launch google", "go to google"}: route = "OPEN_WEBSITE"
    elif re.match(r"^(search google(?: for)?|google search for)\s+.+$", low) or re.match(r"^google\s+.+$", low): route = "GOOGLE_SEARCH"
    elif re.match(r"^play\s+.+$", low): route = "YOUTUBE_PLAY"
    elif re.match(r"^(search youtube(?: for)?|youtube search for|look for .+ on youtube|find .+ on youtube)\s+?.*$", low): route = "YOUTUBE_SEARCH"
    else: route = "GENERAL_LLM"
    return JevDecision(route, 1.0, time.perf_counter() - start, "local")


def route_with_jev(user_text: str) -> JevDecision:
    """Ask Jev for a structured route; safely fall back locally on failure."""
    text = _strip_terminal_punctuation(_clean(user_text))
    start = time.perf_counter()

    local_decision = _local_route(text)
    if local_decision.route == "YOUTUBE_PLAY":
        print(f"[JEV] route=YOUTUBE_PLAY confidence=1.00 latency={local_decision.latency:.3f}s (local guard)")
        return local_decision

    if not JEV_API_KEY:
        decision = local_decision
        print(f"[JEV] unavailable (no TYPESAFE_API_KEY) -> {decision.route}")
        return decision

    payload = {
        "model": JEV_MODEL,
        "state": {
            "utterance": text,
            "context": "Windows desktop voice assistant. Select the safest direct route or GENERAL_LLM.",
        },
        "questions": {
            "route": {
                "type": "choice",
                "instructions": "Which execution route best matches this user's voice command? Choose a direct route only when the intent is clear. Otherwise choose GENERAL_LLM.",
                "criteria": ROUTES,
            }
        },
    }

    try:
        response = requests.post(
            JEV_URL,
            headers={
                "Authorization": f"Bearer {JEV_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=JEV_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        answer = data["answers"]["route"]
        route = str(answer.get("choice", "GENERAL_LLM"))
        confidence = float(answer.get("confidence", 0.0))
        latency = time.perf_counter() - start

        if route not in ROUTES or confidence < JEV_CONFIDENCE_THRESHOLD:
            route = "GENERAL_LLM"

        # Generic deterministic guard: punctuation must not change the meaning
        # of a simple open/launch/go-to command. Resolve known applications and
        # websites locally instead of depending on a probabilistic route.
        normalized = _strip_terminal_punctuation(text).lower()
        explicit_match = re.fullmatch(r"(?:open|launch|start|go to)\s+(.+)", normalized, re.IGNORECASE)
        if explicit_match:
            target = explicit_match.group(1).strip()
            app = APP_ALIASES.get(target)
            website = _website_url(normalized)

            if app:
                route = "OPEN_APPLICATION"
                print("[JEV GUARD] explicit application command -> OPEN_APPLICATION")
                print(f"[JEV] route={route} confidence={confidence:.2f} latency={latency:.3f}s (guarded)")
                return JevDecision(route, confidence, latency, "jev")

            if website:
                route = "OPEN_WEBSITE"
                print("[JEV GUARD] explicit website command -> OPEN_WEBSITE")
                print(f"[JEV] route={route} confidence={confidence:.2f} latency={latency:.3f}s (guarded)")
                return JevDecision(route, confidence, latency, "jev")

        print(f"[JEV] route={route} confidence={confidence:.2f} latency={latency:.3f}s")
        return JevDecision(route, confidence, latency, "jev")

    except Exception as exc:
        latency = time.perf_counter() - start
        decision = _local_route(text)
        print(f"[JEV] API fallback: {type(exc).__name__} after {latency:.3f}s -> {decision.route}")
        return decision


def _extract_google_query(text: str) -> str | None:

    patterns = [
        r"^search google for (.+)$",
        r"^search google (.+)$",
        r"^google search for (.+)$",
        r"^google (.+)$",
    ]

    low = text.lower()

    for pattern in patterns:
        match = re.match(pattern, low)
        if match:
            return _strip_terminal_punctuation(
                text[match.start(1):match.end(1)]
            )

    return None


def _extract_youtube_query(text: str) -> str | None:

    patterns = [
        r"^search youtube for (.+)$",
        r"^search youtube (.+)$",
        r"^youtube search for (.+)$",
        r"^look for (.+) on youtube$",
        r"^find (.+) on youtube$",
    ]

    low = text.lower()

    for pattern in patterns:
        match = re.match(pattern, low)
        if match:
            return _strip_terminal_punctuation(
                text[match.start(1):match.end(1)]
            )

    return None


def _extract_youtube_play(text: str) -> tuple[str, int] | None:
    """Extract YouTube playback requests and optional result index."""
    cleaned = _strip_terminal_punctuation(text)
    low = cleaned.lower()
    ordinal_map = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5}
    match = re.match(r"^play\s+the\s+(\d+)(?:st|nd|rd|th)\s+video\s+(?:of|from|in)\s+(.+)$", low)
    if match:
        return _strip_terminal_punctuation(cleaned[match.start(2):match.end(2)].strip()), max(int(match.group(1)), 1)
    match = re.match(r"^play\s+(?:the\s+)?(first|second|third|fourth|fifth)\s+video\s+(?:of|from|in)\s+(.+)$", low)
    if match:
        return _strip_terminal_punctuation(cleaned[match.start(2):match.end(2)].strip()), ordinal_map[match.group(1)]
    match = re.match(r"^play\s+(.+?)\s+(?:on|from)\s+youtube$", low)
    if match:
        return _strip_terminal_punctuation(cleaned[match.start(1):match.end(1)].strip()), 1
    match = re.match(r"^play\s+(.+)$", low)
    if match:
        query = cleaned[match.start(1):match.end(1)].strip()
        if query: return _strip_terminal_punctuation(query), 1
    return None


def _extract_application(text: str) -> str | None:
    match = re.fullmatch(r"(?:open|launch|start)\s+(.+)", text, re.IGNORECASE)
    if not match:
        return None
    requested = _strip_terminal_punctuation(match.group(1)).lower()
    return APP_ALIASES.get(requested)


def _website_url(text: str) -> str | None:
    low = _strip_terminal_punctuation(text).lower()
    if low in {"open youtube", "launch youtube", "go to youtube"}:
        return "https://www.youtube.com"
    if low in {"open google", "launch google", "go to google"}:
        return "https://www.google.com"

    match = re.fullmatch(r"(?:open|launch|go to)\s+(https?://\S+|(?:www\.)?[\w.-]+\.[a-z]{2,}(?:/\S*)?)", text.strip(), re.IGNORECASE)
    if match:
        url = match.group(1)
        return url if url.startswith(("http://", "https://")) else "https://" + url
    return None


def execute_jev_route(user_text: str, decision: JevDecision):
    """Execute a high-confidence direct route. Return None for LLM fallback."""
    text = _clean(user_text)
    route = decision.route
    start = time.perf_counter()

    if route == "GENERAL_LLM":
        return None
    if route == "SYSTEM_TIME":
        result = f"It's {get_current_time()}."
    elif route == "SYSTEM_DATE":
        result = f"Today is {get_current_date()}."
    elif route == "SYSTEM_BATTERY":
        result = battery_status()
    elif route == "SCREENSHOT":
        result = take_screenshot()
    elif route == "OPEN_APPLICATION":
        app = _extract_application(text)
        result = open_application(app) if app else None
    elif route == "OPEN_WEBSITE":
        url = _website_url(text)
        if not url:
            result = None
        else:
            tool_result = open_website(url)
            if isinstance(tool_result, str) and tool_result.startswith("I couldn't"):
                result = tool_result
            else:
                # Keep internal URLs inside the tool layer; never expose them
                # in the normal JEV user-facing response.
                normalized_url = url.lower().rstrip("/")
                if "youtube.com" in normalized_url:
                    result = "YouTube is open."
                elif "google.com" in normalized_url:
                    result = "Google is open."
                else:
                    result = "The website is open."

    elif route == "GOOGLE_SEARCH":
        query = _extract_google_query(text)
        if not query:
            result = None
        else:
            tool_result = search_web(query)
            if isinstance(tool_result, str) and tool_result.startswith("I couldn't"):
                result = tool_result
            else:
                result = f'Google search opened for "{query}".'

    elif route == "YOUTUBE_SEARCH":
        query = _extract_youtube_query(text)
        if not query:
            return None

        url = "https://www.youtube.com/results?search_query=" + quote_plus(query)
        tool_result = open_website(url)

        if isinstance(tool_result, str) and tool_result.startswith("I couldn't"):
            result = tool_result
        else:
            result = f'YouTube search opened for "{query}".'
    
    elif route == "YOUTUBE_PLAY":
        extracted = _extract_youtube_play(text)

        if not extracted:
            return None

        query, index = extracted

        result = play_youtube(
            query,
            index
        )
    
    else:
        result = None

    elapsed = time.perf_counter() - start
    print(f"[JEV TOOL] route={route} execution={elapsed:.3f}s")
    return result


def execute_jev(user_text: str):
    """Full Jev route + direct execution. None means use OpenAI agent."""
    decision = route_with_jev(user_text)
    return execute_jev_route(user_text, decision)
