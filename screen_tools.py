import base64
from io import BytesIO

import pyautogui
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

MODEL = "gpt-5.6-luna"


def read_screen(mode="text"):
    """
    Capture the current screen and use the vision-capable model
    to read or describe what is visible.
    """

    mode = mode.lower().strip()

    if mode not in {"text", "describe"}:
        return "Mode must be text or describe."

    # Capture the current screen
    screenshot = pyautogui.screenshot()

    # Convert screenshot to PNG bytes
    buffer = BytesIO()
    screenshot.save(buffer, format="PNG")

    # Encode image as base64
    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    if mode == "text":
        instruction = (
            "Read the visible text on this screen. "
            "Extract the important text accurately. "
            "Preserve headings, labels, buttons, and important "
            "information. Do not invent text that is not visible."
        )
    else:
        instruction = (
            "Describe what is currently visible on the screen. "
            "Identify the active application, important UI elements, "
            "visible text, and the main content. "
            "Do not invent information that is not visible."
        )

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": instruction,
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            f"data:image/png;base64,{image_base64}"
                        ),
                    },
                ],
            }
        ],
    )

    return response.output_text