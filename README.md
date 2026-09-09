# AI Voice-Controlled Desktop Assistant

A Python-based AI desktop assistant that lets you control your computer and interact with an AI model using natural voice commands.

The project combines voice activity detection, speech recognition, an LLM with function/tool calling, desktop automation, system monitoring, file utilities, clipboard operations, and text-to-speech into a single voice-driven assistant.

## Project Overview

Unlike a traditional voice assistant that relies on hard-coded commands, this project sends every transcribed request to an LLM. The LLM determines whether the user needs a normal conversational answer or one or more computer tools.

This makes the project a practical example of an **AI agent that can understand natural language and interact with a desktop environment**.

## Architecture

```text
Microphone
    ↓
Silero VAD
    ↓
faster-whisper
    ↓
OpenAI LLM
    ↓
Tool Calling / AI Response
    ↓
Computer Action
    ↓
OpenAI TTS
    ↓
Speaker
```

## Features

### 🎙️ Voice Interaction

- Real-time microphone input
- Streaming voice activity detection using Silero VAD
- Speech-to-text using faster-whisper
- Text-to-speech responses using OpenAI TTS
- Automatic detection of when the user has finished speaking

### 🧠 AI Assistant

- Natural-language understanding
- OpenAI Responses API
- Function/tool calling
- Automatic tool selection based on the user's request
- Support for multiple tool calls in a single request
- Iterative tool execution when additional actions are required
- Normal conversational responses when no computer action is necessary

### 🖥️ Computer Control

- Open applications
- Open websites
- Search the web
- Open folders
- Control system volume
- Mute/unmute audio
- Play/pause media
- Skip to next/previous media
- Minimize/maximize windows
- Take screenshots

### 📊 System Information

- Battery status
- RAM usage
- CPU usage
- Disk usage
- Wi-Fi/internet connectivity
- Screen resolution
- General system information

### 📁 Files and Notes

- Search files on common user folders
- Create timestamped notes
- Read saved notes

### 📋 Clipboard

- Read clipboard contents
- Write text to the clipboard

### 🧮 Utilities

- Calculator
- Current date
- Current time

## Technologies

| Technology | Purpose |
|---|---|
| Python | Core application |
| OpenAI API | LLM reasoning and text-to-speech |
| faster-whisper | Speech recognition |
| Silero VAD | Voice activity detection |
| sounddevice | Microphone input |
| PyAutoGUI | Desktop automation |
| Pyperclip | Clipboard operations |
| psutil | System monitoring |
| playsound3 | Audio playback |
| python-dotenv | Environment variable management |

## Project Structure

```text
Ai-assistant-voice-controlled/
│
├── main.py                    # Main application loop
├── assistant.py               # LLM integration and tool calling
├── tools.py                   # Desktop and system tools
├── wake_word.py               # Voice activity detection and transcription
├── tts.py                     # Text-to-speech
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Git exclusions
```

## How It Works

### 1. Voice Input

The microphone continuously provides short audio chunks to the application.

Silero VAD determines whether the user is speaking and detects the end of the utterance.

### 2. Speech Recognition

The recorded speech is passed to **faster-whisper**, which converts the audio into text.

### 3. AI Reasoning

The transcription is sent to the OpenAI Responses API along with the available tools.

The LLM determines whether it should:

- Answer the user directly
- Call a single tool
- Call multiple tools
- Continue with another tool after receiving a previous tool's result

### 4. Tool Execution

When the LLM requests a function, Python executes the corresponding function in `tools.py`.

Examples include opening applications, checking system information, controlling volume, searching files, and taking screenshots.

### 5. Response

The result of the tool is returned to the LLM.

The LLM then generates a natural-language response, which is converted to speech using OpenAI TTS and played through the speakers.

## Setup

### Prerequisites

- Windows
- Python 3.x
- A working microphone
- Speakers or headphones
- An OpenAI API key

### 1. Clone the repository

```bash
git clone <repository-url>
cd Ai-assistant-voice-controlled
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the OpenAI API key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 6. Run the assistant

```bash
python main.py
```

## Example Commands

The assistant understands natural language rather than requiring exact command phrases.

Examples:

```text
Open Chrome.

What is my battery percentage?

How much RAM am I using?

How much CPU am I using?

How much free storage do I have?

Is my internet working?

What is my screen resolution?

Turn the volume up.

Turn the volume down.

Mute the computer.

Unmute the computer.

Take a screenshot.

Play my music.

Pause the media.

Skip to the next track.

Minimize the current window.

Maximize the current window.

Find my resume.

Create a note saying I have a meeting tomorrow.

Read my notes.

What is currently in my clipboard?

Copy "Hello World" to my clipboard.

What is the current time?

What is today's date?

Calculate 25 * 18.

Open my Downloads folder.
```

The assistant can also answer normal questions conversationally when a computer action is not required.

## Tool Architecture

The project exposes desktop capabilities to the LLM as structured functions.

```text
User Speech
     ↓
Speech-to-Text
     ↓
LLM
     ↓
┌───────────────────────────────┐
│        Tool Selection         │
├───────────────────────────────┤
│ open_application              │
│ open_website                  │
│ search_web                    │
│ system_info                   │
│ battery_status                │
│ memory_usage                  │
│ cpu_usage                     │
│ disk_usage                    │
│ wifi_status                   │
│ screen_resolution             │
│ volume_control                │
│ mute_unmute                   │
│ take_screenshot               │
│ media_control                 │
│ window_control                │
│ search_files                  │
│ create_note                   │
│ read_notes                    │
│ clipboard_get                 │
│ clipboard_set                 │
│ calculate                     │
└───────────────────────────────┘
     ↓
Python Tool Execution
     ↓
Tool Result
     ↓
LLM Response
     ↓
Text-to-Speech
```

## Security

- API keys are stored in `.env` rather than directly in source code.
- `.env` and `.venv/` are excluded through `.gitignore`.
- Generated audio files are excluded from version control.
- The calculator uses a restricted AST-based expression parser instead of executing arbitrary Python code.
- Desktop actions are performed through explicitly defined tools rather than arbitrary code generated by the LLM.

> **Important:** This project can control parts of the local computer. Only run it in an environment where you understand and trust the actions being requested.

## Current Limitations

- The project currently targets Windows desktop automation.
- Speech recognition and LLM responses require local/network resources depending on the component.
- Some applications may use different executable names or require additional handling.
- Browser automation is currently limited compared with a full browser-control agent.
- There is currently no persistent conversation memory across application restarts.
- Sensitive actions do not yet have a dedicated confirmation layer.
- The project does not currently have a graphical user interface.

## Future Improvements

- Conversation memory
- Persistent user preferences
- Persistent long-term memory
- More advanced multi-step reasoning
- Improved application detection
- Confirmation for sensitive computer actions
- Better error recovery
- Action and conversation logging
- Graphical user interface
- Advanced browser automation
- Improved speech interaction
- Wake-word activation
- Configurable voices and assistant personalities
- Better handling of ambiguous user requests

## Development Roadmap

### Phase 1 — Core Voice Pipeline
- [x] Microphone input
- [x] Voice activity detection
- [x] Speech recognition
- [x] Text-to-speech

### Phase 2 — AI Agent
- [x] OpenAI Responses API
- [x] Function/tool calling
- [x] Tool execution
- [x] Multiple tool execution

### Phase 3 — Desktop Capabilities
- [x] Application control
- [x] Website opening
- [x] System monitoring
- [x] Volume and media control
- [x] Window control
- [x] Screenshot capture
- [x] File search
- [x] Notes
- [x] Clipboard operations

### Phase 4 — Advanced Agent Features
- [ ] Conversation memory
- [ ] Persistent preferences
- [ ] Confirmation system
- [ ] Improved error recovery
- [ ] Logging

### Phase 5 — User Interface
- [ ] Graphical user interface
- [ ] Conversation history
- [ ] Visual tool/action status
- [ ] Configuration panel

## Status

**Current Version: Working Prototype**

The core voice → AI → tool → response pipeline is functional and supports a broad set of desktop-control, system-information, file, note, and clipboard operations.

This repository represents the current working foundation for future development into a more capable desktop AI agent.

## License

This project is currently provided for educational and portfolio purposes.

A formal open-source license can be added if the project is later released for public contribution.
