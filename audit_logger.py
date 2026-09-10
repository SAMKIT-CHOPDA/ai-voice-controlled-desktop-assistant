from pathlib import Path
from datetime import datetime, timezone
import json
import re
import uuid


PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "assistant.log"

SESSION_ID = str(uuid.uuid4())


def _sanitize(text):
    """Remove obvious secrets before writing logs."""

    if text is None:
        return None

    text = str(text)

    # API keys / common secret patterns
    text = re.sub(
        r"(sk-[A-Za-z0-9_-]+)",
        "[REDACTED_API_KEY]",
        text
    )

    # Password/token/secret assignments
    text = re.sub(
        r"(?i)(password|passwd|token|secret|api[_-]?key)\s*[:=]\s*[^\s,]+",
        r"\1=[REDACTED]",
        text
    )

    return text


def _write_log(entry):
    LOG_DIR.mkdir(exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(entry, ensure_ascii=False)
            + "\n"
        )


def log_request(user_request):
    """Log a user request."""

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": SESSION_ID,
        "event": "request",
        "user_request": _sanitize(user_request),
    }

    _write_log(entry)


def log_response(response, status="success", duration=None):
    """Log an assistant response."""

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": SESSION_ID,
        "event": "response",
        "status": status,
        "assistant_response": _sanitize(response),
    }

    if duration is not None:
        entry["duration_seconds"] = round(duration, 3)

    _write_log(entry)


def log_error(error):
    """Log an error without exposing sensitive information."""

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": SESSION_ID,
        "event": "error",
        "error": _sanitize(str(error)),
    }

    _write_log(entry)


def get_log_file():
    """Return the location of the audit log."""

    return str(LOG_FILE)