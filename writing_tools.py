# =============================================================
# WRITING ASSISTANT TOOLS
# =============================================================


def improve_writing(text, style="clear"):
    text = text.strip()

    if not text:
        return "Please provide some text to improve."

    style = style.lower().strip()

    allowed_styles = {
        "clear",
        "formal",
        "professional",
        "academic",
        "simple",
        "natural"
    }

    if style not in allowed_styles:
        return (
            "Style must be clear, formal, professional, "
            "academic, simple, or natural."
        )

    return (
        f"Improve the following text in a {style} style. "
        "Preserve the original meaning while improving grammar, "
        "clarity, vocabulary, and sentence structure where appropriate.\n\n"
        f"Text:\n{text}"
    )


def correct_grammar(text):
    text = text.strip()

    if not text:
        return "Please provide some text to correct."

    return (
        "Correct the grammar, spelling, punctuation, and sentence "
        "structure of the following text. Preserve the original "
        "meaning and do not unnecessarily change the wording.\n\n"
        f"Text:\n{text}"
    )


def paraphrase_text(text, style="natural"):
    text = text.strip()

    if not text:
        return "Please provide some text to paraphrase."

    style = style.lower().strip()

    allowed_styles = {
        "natural",
        "formal",
        "academic",
        "simple"
    }

    if style not in allowed_styles:
        return (
            "Style must be natural, formal, academic, or simple."
        )

    return (
        f"Paraphrase the following text in a {style} style. "
        "Keep the original meaning but use different wording "
        "and sentence structure.\n\n"
        f"Text:\n{text}"
    )


def summarize_text(text, length="short"):
    text = text.strip()

    if not text:
        return "Please provide some text to summarize."

    length = length.lower().strip()

    allowed_lengths = {
        "short",
        "medium",
        "detailed"
    }

    if length not in allowed_lengths:
        return "Length must be short, medium, or detailed."

    return (
        f"Summarize the following text in a {length} format. "
        "Keep the most important information and remove unnecessary "
        "details.\n\n"
        f"Text:\n{text}"
    )


def write_email(purpose, tone="professional"):
    purpose = purpose.strip()

    if not purpose:
        return "Please provide the purpose of the email."

    tone = tone.lower().strip()

    allowed_tones = {
        "professional",
        "formal",
        "friendly",
        "polite",
        "casual"
    }

    if tone not in allowed_tones:
        return (
            "Tone must be professional, formal, friendly, "
            "polite, or casual."
        )

    return (
        f"Write a {tone} email based on the following purpose. "
        "Include an appropriate subject line, greeting, concise "
        "body, and closing. Do not invent personal details.\n\n"
        f"Purpose:\n{purpose}"
    )