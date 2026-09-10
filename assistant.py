import json
import os
from urllib import response

from dotenv import load_dotenv
from openai import OpenAI
from document_tools import find_document, read_document
from file_organization_tools import organize_folder
from screen_tools import read_screen

from memory_tools import (
    save_memory,
    search_memory,
    read_memories,
    delete_memory
)

from study_tools import (
    create_quiz,
    explain_topic,
    generate_study_questions,
    evaluate_answer
)

from writing_tools import (
    improve_writing,
    correct_grammar,
    paraphrase_text,
    summarize_text,
    write_email
)

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
13. When the user asks for current, recent, live, latest, or up-to-date
    information, use hosted web search.
14. When the user asks to research, investigate, analyze, compare, or
    summarize a topic using current information, treat it as a research task.
15. For research tasks, perform multiple focused web searches when useful.
    Do not rely on a single search when the topic has multiple important
    aspects.
16. For broad research questions, break the topic into useful subtopics
    before searching.
17. Use the retrieved web information as evidence. Do not invent facts,
    sources, statistics, dates, or developments that were not supported by
    the retrieved information.
18. When presenting research findings, prioritize the most important
    information first and clearly distinguish established facts from
    uncertain or conflicting information.
19. For comparisons, research the relevant options separately when
    necessary and then compare them using the retrieved evidence.
20. If the user asks for a research summary, give a concise spoken summary
    containing the key findings rather than reading a long article.
21. Do not claim that you searched the web if you did not actually retrieve
    search results.
22. For multi-step tasks, continue using available tools until the request
    is completed or no further tool is necessary.
23. Match research depth to the user's request:
    - Simple current question: use a small number of searches.
    - Broad research request: use several focused searches.
    - Detailed comparison or investigation: research each major aspect
      before forming the final answer.
24. When the user asks to find a document, PDF, Word file, or text file,
    use find_document.
25. When the user asks to read, summarize, analyze, or answer questions
    about a document, use find_document first if the file path is not
    already known, then use read_document.
26. Only use read_document for supported document types: PDF, DOCX, and TXT.
27. When a document is very long, focus on the relevant information and
    give a concise spoken response rather than reading the entire document.
28. When the user asks to organize files, use organize_folder with
    confirmed=false first to show the proposed changes.
29. Never use confirmed=true unless the user has explicitly confirmed
    that they want the proposed file changes performed.
30. Do not interpret a general request such as "organize my Downloads"
    as permission to immediately move files.
31. If the user explicitly confirms the proposed organization, use
    organize_folder with confirmed=true.
32. Use save_memory when the user explicitly asks you to remember
    a useful fact, preference, instruction, or piece of information
    for future conversations.
33. Use search_memory when information from long-term memory could
    help answer the user's current request.
34. Use read_memories when the user asks what you remember about them.
35. Use delete_memory when the user explicitly asks you to forget
    a saved memory.
36. Do not save every statement the user makes. Only save information
    that is clearly useful for future interactions or explicitly
    requested to be remembered.
37. Do not reveal or discuss the internal memory system unless the
    user asks about it.
38. When the user asks to be quizzed on a topic, use create_quiz.
39. When the user asks for an explanation of a topic for studying,
    use explain_topic.
40. When the user asks for practice questions, use
    generate_study_questions.
41. When the user provides an answer to a study question and asks
    for evaluation, use evaluate_answer.
42. During an interactive quiz, ask one question at a time and wait
    for the user's answer before continuing.
43. When evaluating an answer, clearly explain whether it is correct,
    partially correct, or incorrect, and briefly explain why.
44. Keep study responses appropriate for spoken conversation and
    avoid unnecessarily long explanations unless the user asks
    for detail.
45. When the user asks to improve, rewrite, or polish text, use
    improve_writing.
46. When the user asks to correct grammar, spelling, punctuation,
    or sentence structure, use correct_grammar.
47. When the user asks to paraphrase text, use paraphrase_text.
48. When the user asks for a summary of provided text, use
    summarize_text.
49. When the user asks to write an email, use write_email.
50. Preserve the user's original meaning when editing or
    paraphrasing text.
51. Do not invent personal details, names, dates, facts, or
    experiences when writing emails or other personal content.
52. Keep writing responses appropriate for spoken conversation
    unless the user explicitly asks for a longer written output.
53. Use read_screen with mode "text" when the user asks you to read,
    extract, or identify text visible on the current screen.
54. Use read_screen with mode "describe" when the user asks what is
    currently on the screen, what application is open, or asks you
    to describe or inspect the current screen.
55. Use take_screenshot when the user specifically asks to take,
    capture, or save a screenshot.
56. Do not use take_screenshot when the user wants you to understand
    or read the current screen; use read_screen instead.

Important tool rules:

- Use system-information tools when the user asks about the computer's
  battery, RAM, CPU, storage, network, or display.
- Use volume_control for increasing or decreasing volume.
- Use mute_unmute when the user explicitly asks to mute or unmute.
- Use take_screenshot when the user asks for a screenshot.
- Use read_screen with mode "text" when the user asks you to read or extract text visible on the current screen.
- Use read_screen with mode "describe" when the user asks what is on the screen, what application is open, or asks you to describe or inspect the current screen.
- Do not use take_screenshot when the user wants you to understand or read the screen; use read_screen instead.
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
    
        {
        "type": "web_search"
    },
        
    
        
    # ---------------------------------------------------------
    # SAVE MEMORY
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "save_memory",
        "description": (
            "Save a useful fact, preference, instruction, or other "
            "information for future conversations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": (
                        "The information that should be permanently remembered."
                    )
                }
            },
            "required": ["memory"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # SEARCH MEMORY
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "search_memory",
        "description": (
            "Search the assistant's long-term memory for information "
            "relevant to the user's request."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The topic or information to search for."
                    )
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # READ MEMORIES
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "read_memories",
        "description": (
            "Read all information currently stored in long-term memory."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # DELETE MEMORY
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "delete_memory",
        "description": (
            "Delete a specific saved memory when the user explicitly "
            "asks the assistant to forget it."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "memory": {
                    "type": "string",
                    "description": (
                        "The exact memory that should be forgotten."
                    )
                }
            },
            "required": ["memory"],
            "additionalProperties": False
        },
        "strict": True
    },
        
    
    # ---------------------------------------------------------
    # FIND DOCUMENT
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "find_document",
        "description": (
            "Find PDF, DOCX, or TXT documents in the user's "
            "Desktop, Documents, and Downloads folders."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The document filename or part of the filename "
                        "to search for."
                    )
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # READ DOCUMENT
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "read_document",
        "description": (
            "Extract readable text from a PDF, DOCX, or TXT document "
            "using its full file path."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The complete path to the document."
                }
            },
            "required": ["path"],
            "additionalProperties": False
        },
        "strict": True
    },
    
    # ---------------------------------------------------------
    # CREATE QUIZ
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "create_quiz",
        "description": (
            "Start an interactive quiz on a study topic."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic for the quiz."
                },
                "number_of_questions": {
                    "type": "integer",
                    "description": "Number of questions, from 1 to 20."
                },
                "difficulty": {
                    "type": "string",
                    "description": "Quiz difficulty: easy, medium, or hard."
                }
            },
            "required": [
                "topic",
                "number_of_questions",
                "difficulty"
            ],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # EXPLAIN TOPIC
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "explain_topic",
        "description": (
            "Explain a study topic at a selected difficulty level."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic to explain."
                },
                "level": {
                    "type": "string",
                    "description": (
                        "Explanation level: beginner, intermediate, "
                        "or advanced."
                    )
                }
            },
            "required": ["topic", "level"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # STUDY QUESTIONS
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "generate_study_questions",
        "description": (
            "Generate practice questions for a study topic."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The study topic."
                },
                "number_of_questions": {
                    "type": "integer",
                    "description": "Number of questions, from 1 to 20."
                }
            },
            "required": [
                "topic",
                "number_of_questions"
            ],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # EVALUATE ANSWER
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "evaluate_answer",
        "description": (
            "Evaluate a student's answer to a study question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The study question."
                },
                "answer": {
                    "type": "string",
                    "description": "The student's answer."
                }
            },
            "required": ["question", "answer"],
            "additionalProperties": False
        },
        "strict": True
    },
    
    # ---------------------------------------------------------
    # IMPROVE WRITING
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "improve_writing",
        "description": "Improve provided text while preserving its meaning.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to improve."
                },
                "style": {
                    "type": "string",
                    "description": (
                        "Writing style: clear, formal, professional, "
                        "academic, simple, or natural."
                    )
                }
            },
            "required": ["text", "style"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # GRAMMAR CORRECTION
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "correct_grammar",
        "description": "Correct grammar, spelling, punctuation, and sentence structure.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to correct."
                }
            },
            "required": ["text"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # PARAPHRASE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "paraphrase_text",
        "description": "Paraphrase provided text while preserving its meaning.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to paraphrase."
                },
                "style": {
                    "type": "string",
                    "description": (
                        "Paraphrasing style: natural, formal, "
                        "academic, or simple."
                    )
                }
            },
            "required": ["text", "style"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # SUMMARIZE
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "summarize_text",
        "description": "Summarize provided text.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to summarize."
                },
                "length": {
                    "type": "string",
                    "description": "Summary length: short, medium, or detailed."
                }
            },
            "required": ["text", "length"],
            "additionalProperties": False
        },
        "strict": True
    },


    # ---------------------------------------------------------
    # WRITE EMAIL
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "write_email",
        "description": "Write an email based on a user's purpose.",
        "parameters": {
            "type": "object",
            "properties": {
                "purpose": {
                    "type": "string",
                    "description": "The purpose or situation for the email."
                },
                "tone": {
                    "type": "string",
                    "description": (
                        "Email tone: professional, formal, friendly, "
                        "polite, or casual."
                    )
                }
            },
            "required": ["purpose", "tone"],
            "additionalProperties": False
        },
        "strict": True
    },
    
    # ---------------------------------------------------------
    # FILE ORGANIZATION
    # ---------------------------------------------------------

    {
        "type": "function",
        "name": "organize_folder",
        "description": (
            "Analyze and organize files in a folder by category. "
            "Use confirmed=false to preview proposed changes. "
            "Files are only moved when confirmed=true."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": (
                        "The complete path of the folder to organize."
                    )
                },
                "confirmed": {
                    "type": "boolean",
                    "description": (
                        "Set to true only when the user has explicitly "
                        "confirmed that the proposed organization should "
                        "be performed."
                    )
                }
            },
            "required": ["folder", "confirmed"],
            "additionalProperties": False
        },
        "strict": True
    },

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
    
    {
        "type": "function",
        "name": "read_screen",
        "description": (
            "Capture and analyze the current screen using vision. "
            "Use this when the user asks to read, understand, "
            "describe, or inspect what is currently visible on the screen."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["text", "describe"],
                    "description": (
                        "Use 'text' to extract visible text. "
                        "Use 'describe' to describe the screen, "
                        "including the active application and important UI elements."
                    )
                }
            },
            "required": ["mode"],
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
        
    MAX_TOOL_ROUNDS = 5
    tool_round = 0

    while True:
        tool_round += 1

        if tool_round > MAX_TOOL_ROUNDS:
            conversation_response_id = response.id
            return "I reached the maximum number of steps while processing your request."

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # -----------------------------------------------------
        # Hosted web search is already handled by OpenAI
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
                
            elif call.name == "read_screen":
                result = read_screen(arguments["mode"])

            elif call.name == "media_control":

                result = media_control(
                    arguments["action"]
                )

            elif call.name == "window_control":

                result = window_control(
                    arguments["action"]
                )

            # -------------------------------------------------
            # DOCUMENTS
            # -------------------------------------------------

            elif call.name == "find_document":

                result = find_document(
                    arguments["query"]
                )

            elif call.name == "read_document":

                result = read_document(
                    arguments["path"]
                )
                
                
            # -------------------------------------------------
            # FILE ORGANIZATION
            # -------------------------------------------------

            elif call.name == "organize_folder":

                result = organize_folder(
                    arguments["folder"],
                    arguments["confirmed"]
                )    
            
            # -------------------------------------------------
            # LONG-TERM MEMORY
            # -------------------------------------------------

            elif call.name == "save_memory":

                result = save_memory(
                    arguments["memory"]
                )

            elif call.name == "search_memory":

                result = search_memory(
                    arguments["query"]
                )

            elif call.name == "read_memories":

                result = read_memories()

            elif call.name == "delete_memory":

                result = delete_memory(
                    arguments["memory"]
                )
                
            # -------------------------------------------------
            # STUDY ASSISTANT
            # -------------------------------------------------

            elif call.name == "create_quiz":

                result = create_quiz(
                    arguments["topic"],
                    arguments["number_of_questions"],
                    arguments["difficulty"]
                )

            elif call.name == "explain_topic":

                result = explain_topic(
                    arguments["topic"],
                    arguments["level"]
                )

            elif call.name == "generate_study_questions":

                result = generate_study_questions(
                    arguments["topic"],
                    arguments["number_of_questions"]
                )

            elif call.name == "evaluate_answer":

                result = evaluate_answer(
                    arguments["question"],
                    arguments["answer"]
                )
                
            # -------------------------------------------------
            # WRITING ASSISTANT
            # -------------------------------------------------

            elif call.name == "improve_writing":

                result = improve_writing(
                    arguments["text"],
                    arguments["style"]
                )

            elif call.name == "correct_grammar":

                result = correct_grammar(
                    arguments["text"]
                )

            elif call.name == "paraphrase_text":

                result = paraphrase_text(
                    arguments["text"],
                    arguments["style"]
                )

            elif call.name == "summarize_text":

                result = summarize_text(
                    arguments["text"],
                    arguments["length"]
                )

            elif call.name == "write_email":

                result = write_email(
                    arguments["purpose"],
                    arguments["tone"]
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