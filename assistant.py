import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    open_application,
    open_website,
    search_web,
    get_current_time,
    get_current_date,
    system_info,
    open_folder,
    calculate,
    battery_status,
    memory_usage,
    cpu_usage,
    disk_usage,
    wifi_status,
    screen_resolution,
    volume_control,
    mute_unmute,
    take_screenshot,
    media_control,
    window_control,
    search_files,
    create_note,
    read_notes,
    clipboard_get,
    clipboard_set
)


# =============================================================
# OPENAI SETUP
# =============================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-5.6-luna"

# Stores the latest response ID for conversation memory
conversation_response_id = None


# =============================================================
# SYSTEM PROMPT
# =============================================================

SYSTEM_PROMPT = """
You are a professional desktop voice assistant.

The user communicates with you through speech.

Your responsibilities:

1. Understand the user's request.
2. If the request requires controlling the computer, use an appropriate tool.
3. If the request requires current system information, use the appropriate tool.
4. If the request requires an exact mathematical calculation, use the calculator tool.
5. If the request requires accessing or modifying the clipboard, use the appropriate tool.
6. If the request requires creating or reading notes, use the appropriate tool.
7. If the request requires finding files, use the file search tool.
8. If the request is a normal question, answer it directly.
9. Do not use tools when they are unnecessary.
10. Keep spoken responses concise and natural.
11. Do not mention internal tools, function calls, APIs, or system architecture
    unless the user specifically asks.
12. The user speaks English.

Important tool rules:

- Use system-information tools when the user asks about the computer's
  battery, RAM, CPU, storage, network, or display.
- Use volume_control for increasing or decreasing volume.
- Use mute_unmute when the user explicitly asks to mute or unmute.
- Use take_screenshot when the user asks for a screenshot.
- Use media_control for play, pause, next track, or previous track.
- Use window_control for minimizing, maximizing, or restoring the active window.
- Use search_files when the user asks to find a file.
- Use create_note when the user asks you to remember something by saving a note.
- Use read_notes when the user asks about saved notes.
- Use clipboard_get when the user asks what is currently copied.
- Use clipboard_set when the user asks you to copy something.
"""


# =============================================================
# TOOL DEFINITIONS
# =============================================================

TOOLS = [

    # ---------------------------------------------------------
    # OPEN APPLICATION
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "open_application",
        "description": "Open an installed application on the Windows computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": "string",
                    "description": (
                        "The application to open, such as Chrome, "
                        "Notepad, Calculator, Edge, or File Explorer."
                    )
                }
            },
            "required": ["application"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # OPEN WEBSITE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "open_website",
        "description": "Open a website in the default browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The complete website URL."
                }
            },
            "required": ["url"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # SEARCH WEB
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "search_web",
        "description": "Search Google for information requested by the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # CURRENT TIME
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current local time of the computer.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # CURRENT DATE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "get_current_date",
        "description": "Get the current local date of the computer.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # SYSTEM INFORMATION
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "system_info",
        "description": (
            "Get basic information about the computer, including "
            "operating system, computer name, and processor."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # OPEN FOLDER
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "open_folder",
        "description": (
            "Open a common Windows folder such as Downloads, "
            "Documents, Desktop, Pictures, Music, or Videos."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": (
                        "The folder to open. Examples: Downloads, "
                        "Documents, Desktop, Pictures, Music, Videos."
                    )
                }
            },
            "required": ["folder"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # CALCULATOR
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "calculate",
        "description": (
            "Perform an exact mathematical calculation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A mathematical expression such as "
                        "25 * 4, 100 / 5, or (12 + 8) * 3."
                    )
                }
            },
            "required": ["expression"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # BATTERY STATUS
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "battery_status",
        "description": "Check the current battery percentage and charging state.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # MEMORY USAGE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "memory_usage",
        "description": "Check the current RAM usage of the computer.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # CPU USAGE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "cpu_usage",
        "description": "Check the current CPU utilization.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # DISK USAGE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "disk_usage",
        "description": "Check total, used, and free disk storage.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # WIFI STATUS
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "wifi_status",
        "description": "Check the current network and internet connection status.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # SCREEN RESOLUTION
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "screen_resolution",
        "description": "Get the current screen resolution.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # VOLUME CONTROL
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "volume_control",
        "description": (
            "Control the computer's volume by increasing, "
            "decreasing, muting, or unmuting it."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": (
                        "The volume action: up, down, mute, or unmute."
                    )
                }
            },
            "required": ["action"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # MUTE / UNMUTE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "mute_unmute",
        "description": "Mute or unmute the computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Either mute or unmute."
                }
            },
            "required": ["action"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # SCREENSHOT
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "take_screenshot",
        "description": "Take a screenshot of the current screen.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # MEDIA CONTROL
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "media_control",
        "description": (
            "Control media playback using play/pause, next track, "
            "or previous track."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": (
                        "The media action: play, pause, next, or previous."
                    )
                }
            },
            "required": ["action"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # WINDOW CONTROL
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "window_control",
        "description": (
            "Control the currently active window by minimizing, "
            "maximizing, or restoring it."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": (
                        "The window action: minimize, maximize, or restore."
                    )
                }
            },
            "required": ["action"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # FILE SEARCH
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "search_files",
        "description": (
            "Search common user folders for files matching a filename."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The filename or part of the filename to search for."
                    )
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # CREATE NOTE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "create_note",
        "description": "Save a note to the assistant's notes file.",
        "parameters": {
            "type": "object",
            "properties": {
                "note": {
                    "type": "string",
                    "description": "The content of the note to save."
                }
            },
            "required": ["note"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # READ NOTES
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "read_notes",
        "description": "Read the notes previously saved by the assistant.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # CLIPBOARD GET
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "clipboard_get",
        "description": "Read the current text stored in the clipboard.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # CLIPBOARD SET
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "clipboard_set",
        "description": "Copy text to the computer's clipboard.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to copy to the clipboard."
                }
            },
            "required": ["text"],
            "additionalProperties": False
        },
        "strict": True
    }
]


# =============================================================
# LLM FUNCTION
# =============================================================

def ask_llm(user_text):

    global conversation_response_id

    if conversation_response_id is None:

        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            tools=TOOLS,
            input=user_text
        )

    else:

        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            tools=TOOLS,
            previous_response_id=conversation_response_id,
            input=user_text
        )

    while True:

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # -----------------------------------------------------
        # No tool required
        # -----------------------------------------------------

        if not tool_calls:

            conversation_response_id = response.id

            return response.output_text

        # -----------------------------------------------------
        # Execute tools
        # -----------------------------------------------------
        
        tool_outputs = []

        for call in tool_calls:

            arguments = json.loads(call.arguments)

            print()
            print("Tool:", call.name)
            print("Arguments:", arguments)

            # -------------------------------------------------
            # BASIC TOOLS
            # -------------------------------------------------

            if call.name == "open_application":

                result = open_application(
                    arguments["application"]
                )

            elif call.name == "open_website":

                result = open_website(
                    arguments["url"]
                )

            elif call.name == "search_web":

                result = search_web(
                    arguments["query"]
                )

            elif call.name == "get_current_time":

                result = get_current_time()

            elif call.name == "get_current_date":

                result = get_current_date()

            elif call.name == "system_info":

                result = system_info()

            elif call.name == "open_folder":

                result = open_folder(
                    arguments["folder"]
                )

            elif call.name == "calculate":

                result = calculate(
                    arguments["expression"]
                )

            # -------------------------------------------------
            # SYSTEM STATUS
            # -------------------------------------------------

            elif call.name == "battery_status":

                result = battery_status()

            elif call.name == "memory_usage":

                result = memory_usage()

            elif call.name == "cpu_usage":

                result = cpu_usage()

            elif call.name == "disk_usage":

                result = disk_usage()

            elif call.name == "wifi_status":

                result = wifi_status()

            elif call.name == "screen_resolution":

                result = screen_resolution()

            # -------------------------------------------------
            # COMPUTER CONTROL
            # -------------------------------------------------

            elif call.name == "volume_control":

                result = volume_control(
                    arguments["action"]
                )

            elif call.name == "mute_unmute":

                result = mute_unmute(
                    arguments["action"]
                )

            elif call.name == "take_screenshot":

                result = take_screenshot()

            elif call.name == "media_control":

                result = media_control(
                    arguments["action"]
                )

            elif call.name == "window_control":

                result = window_control(
                    arguments["action"]
                )

            # -------------------------------------------------
            # FILES & NOTES
            # -------------------------------------------------

            elif call.name == "search_files":

                result = search_files(
                    arguments["query"]
                )

            elif call.name == "create_note":

                result = create_note(
                    arguments["note"]
                )

            elif call.name == "read_notes":

                result = read_notes()

            # -------------------------------------------------
            # CLIPBOARD
            # -------------------------------------------------

            elif call.name == "clipboard_get":

                result = clipboard_get()

            elif call.name == "clipboard_set":

                result = clipboard_set(
                    arguments["text"]
                )

            # -------------------------------------------------
            # UNKNOWN TOOL
            # -------------------------------------------------

            else:

                result = "Unknown tool."

            # -------------------------------------------------
            # Send tool result back to the LLM
            # -------------------------------------------------

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result
            })

        # -----------------------------------------------------
        # Ask LLM for final response
        # -----------------------------------------------------

        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            tools=TOOLS,
            previous_response_id=response.id,
            input=tool_outputs
        )
        
def reset_conversation():

    global conversation_response_id

    conversation_response_id = None