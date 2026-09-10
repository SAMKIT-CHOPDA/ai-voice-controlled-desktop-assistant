# AI Voice-Controlled Desktop Assistant

> A voice-driven AI agent for Windows that combines speech recognition, LLM reasoning, tool calling, desktop automation, web research, document understanding, file organization, memory, study assistance, and writing assistance.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/LLM-OpenAI-black?logo=openai&logoColor=white)](https://openai.com/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange)]()

---

## 📌 Overview

This project is a Python-based AI desktop assistant designed to understand natural voice commands and take useful actions on a Windows computer.

Unlike traditional assistants that depend primarily on fixed commands, every transcribed request is sent to an LLM. The model decides whether to:

- Answer conversationally
- Search the web
- Call one or more desktop tools
- Read a local document
- Organize files
- Retrieve or store long-term memory
- Provide study assistance
- Perform writing tasks

The result is a practical implementation of a **tool-using AI agent** capable of reasoning about requests and interacting with the local desktop environment.

---

# ✨ Key Features

### 🎙️ Voice Interaction
- Real-time microphone input
- Silero VAD for speech detection
- faster-whisper for speech-to-text
- OpenAI TTS for voice responses
- Automatic detection of the end of an utterance

### 🧠 AI Agent
- OpenAI Responses API
- Function/tool calling
- Automatic tool selection
- Multiple tool calls
- Iterative tool execution
- Multi-turn conversational context

### 🔎 Smart Research
- Current web research
- Hosted web search
- Multi-step research

### 📄 Document Understanding
- PDF reading
- DOCX reading
- TXT reading
- Document search across common Windows folders

### 📁 Smart File Organization
- Categorizes files into Documents, Images, Videos, Audio, and Archives
- Preview before execution
- Explicit confirmation before moving files
- Duplicate filename handling

### 🧠 Long-Term Memory
- Save useful preferences and instructions
- Search memories
- Read memories
- Delete memories
- Persistent local JSON storage

### 📚 Study Assistant
- Topic explanations
- Practice questions
- Interactive quizzes
- Answer evaluation

### ✍️ Writing Assistant
- Writing improvement
- Grammar correction
- Paraphrasing
- Summarization
- Email generation

### 🖥️ Desktop Control
- Open applications
- Open websites
- Open folders
- Volume control
- Mute/unmute
- Media controls
- Window controls
- Screenshots
- Screen understanding
- Mouse movement and clicking
- Double-clicking
- Text typing
- Keyboard keys and hotkeys
- Scrolling and drag operations
- Mouse position detection

### 📊 System Monitoring
- Battery status
- RAM usage
- CPU usage
- Disk usage
- Wi-Fi/internet status
- Screen resolution
- General system information
- Context-aware system notifications
- Background system monitoring

### 📋 Productivity
- File search
- Notes
- Clipboard operations
- Calculator
- Date and time

### ⚙️ Smart Process Management
- List running processes
- Find processes by name
- Inspect process details
- Identify top CPU-consuming processes
- Identify top memory-consuming processes
- Close processes
- Restart processes

### 👨‍💻 Developer Assistant
- Inspect project structure
- Read project files
- Search project code
- Modify project files when explicitly requested
- Run Python files
- Run Python commands
- Check Git status
- Inspect Git differences

### 🐍 Python Environment & Package Management
- Python environment information
- List installed packages
- Inspect package information
- Check package availability
- Check Python modules
- Install packages when explicitly requested
- Uninstall packages when explicitly requested
- Upgrade packages when explicitly requested
- Generate requirements files
- Verify project requirements

### 📝 Audit & Request Logging
- Records user requests
- Records assistant responses
- Records success/error status
- Records processing duration
- Generates session identifiers
- Sanitizes common secrets before logging
- Stores logs locally in JSON Lines format
- Keeps logs outside Git through `.gitignore`

---

# 🏗️ Architecture

```text
                 ┌─────────────────┐
                 │   Microphone    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │    Silero VAD   │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │  faster-whisper │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │   OpenAI LLM    │
                 │  Agent Reasoning│
                 └────────┬────────┘
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
       Direct Answer             Tool Selection
                                      ↓
       ┌─────────────────────────────────────────┐
       │ Desktop │ Web │ Documents │ Files      │
       │ Memory  │ Study │ Writing │ System     │
       └────────────────────┬────────────────────┘
                            ↓
                       Tool Result
                            ↓
                      OpenAI LLM
                            ↓
                      OpenAI TTS
                            ↓
                         Speaker
```

---

# 🧩 Tool Architecture

The assistant exposes capabilities to the LLM as structured functions.

```text
User Speech
     ↓
Speech-to-Text
     ↓
LLM
     ↓
Tool Selection
     ↓
┌────────────────────────────────────┐
│ Desktop Tools                      │
│ System Tools                       │
│ Web Search                         │
│ Document Tools                     │
│ File Organization Tools            │
│ Memory Tools                       │
│ Study Tools                        │
│ Writing Tools                      │
└──────────────────┬─────────────────┘
                   ↓
             Python Execution
                   ↓
              Tool Result
                   ↓
                  LLM
                   ↓
            Final Response
                   ↓
             Text-to-Speech
```

---

# 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Core application |
| OpenAI Responses API | LLM reasoning and tool calling |
| OpenAI TTS | Voice responses |
| faster-whisper | Speech recognition |
| Silero VAD | Voice activity detection |
| sounddevice | Microphone input |
| PyAutoGUI | Desktop automation |
| Pyperclip | Clipboard operations |
| psutil | System monitoring |
| PyMuPDF | PDF extraction |
| python-docx | DOCX extraction |
| playsound3 | Audio playback |
| python-dotenv | Environment configuration |
| PySide6 | Desktop graphical user interface (planned) |

---

# 📂 Project Structure

```text
Ai-assistant-voice-controlled/
│
├── main.py
├── assistant.py
├── tools.py
├── wake_word.py
├── tts.py
│
├── document_tools.py
├── file_organization_tools.py
├── memory_tools.py
├── study_tools.py
├── writing_tools.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

| File | Purpose |
|---|---|
| `main.py` | Main voice assistant loop |
| `assistant.py` | LLM integration and tool orchestration |
| `tools.py` | Desktop, system, clipboard, notes and utility tools |
| `wake_word.py` | Voice activity detection and speech recognition |
| `tts.py` | Text-to-speech |
| `document_tools.py` | PDF, DOCX and TXT document handling |
| `file_organization_tools.py` | Safe file organization |
| `memory_tools.py` | Persistent long-term memory |
| `study_tools.py` | Study and quiz functionality |
| `writing_tools.py` | Writing assistance |
| `screen_tools.py` | Screen reading and visual understanding |
| `gui_tools.py` | Mouse and keyboard automation |
| `notification_tools.py` | Notifications and system monitoring |
| `developer_tools.py` | Developer/project assistant capabilities |
| `environment_tools.py` | Python environment and package management |
| `process_tools.py` | Running-process inspection and management |
| `audit_logger.py` | Secure local request/response audit logging |

---

# 🔄 How It Works

### 1. Voice Input

The microphone continuously supplies audio data.

Silero VAD detects speech and determines when the user has finished speaking.

### 2. Speech Recognition

The recorded audio is transcribed using faster-whisper.

```text
Audio → faster-whisper → Text
```

### 3. Agent Reasoning

The transcription is sent to the OpenAI Responses API together with the available tools.

The LLM determines whether to answer directly or call one or more tools.

### 4. Tool Execution

Python executes the requested tool.

For example:

```text
User:
"How much RAM am I using?"

        ↓

LLM selects:
memory_usage()

        ↓

Python executes the function

        ↓

Tool result returned to LLM

        ↓

LLM generates final response
```

### 5. Voice Response

The final response is converted to speech using OpenAI TTS and played through the speakers.

### 6. Audit Logging

Every request sent through `ask_llm()` is recorded locally together with the assistant response, status, and processing duration.

Logs are stored in:

```text
logs/assistant.log
```

The log uses JSON Lines format so individual requests can be inspected or processed by the future graphical interface. Common secrets are sanitized before being written, and the `logs/` directory is excluded from Git.

---

# 🎯 Example Commands

The assistant understands natural language rather than requiring exact command phrases.

### Desktop

```text
Open Chrome.
Open my Downloads folder.
Take a screenshot.
Minimize the current window.
Turn the volume up.
Pause the media.
```

### System

```text
What is my battery percentage?
How much RAM am I using?
How much CPU am I using?
How much free storage do I have?
Is my internet working?
```

### Documents & Files

```text
Find my resume.
Read my project report.
Summarize my PDF.
Organize my Downloads folder.
Show me what files would be organized.
```

### Research

```text
Research the latest developments in AI agents.
Compare current AI models.
Find the latest information about a technology.
```

### Memory

```text
Remember that I prefer concise answers.
What do you remember about me?
Forget that preference.
```

### Study

```text
Explain neural networks at a beginner level.
Give me practice questions about machine learning.
Quiz me on Python OOP.
Evaluate my answer.
```

### Writing

```text
Improve this paragraph in a formal style.
Correct my grammar.
Paraphrase this paragraph academically.
Summarize this text.
Write a professional email.
```

---

# 🔐 Safety

The project includes several safety-oriented design choices:

- API keys are stored in `.env`
- `.env` is excluded from Git
- `.venv/` is excluded from Git
- Generated audio files are excluded from Git
- The calculator uses a restricted AST-based expression parser
- Desktop actions are performed through explicitly defined tools
- File organization uses a preview-before-execution workflow
- File organization requires explicit confirmation before moving files
- The LLM cannot directly execute arbitrary Python code through the tool system
- Developer tools are restricted to the project directory
- Protected project areas such as `.env`, `.git`, and `.venv` are guarded
- Package installation/removal/upgrades require explicit user requests
- Audit logs sanitize common secret patterns
- Audit logs are excluded from Git

> **Important:** This project can control parts of the local computer. Only run it in an environment where you understand and trust the requested actions.

---

# 🚀 Installation

## Prerequisites

- Windows
- Python 3.x
- Working microphone
- Speakers or headphones
- OpenAI API key

## 1. Clone

```bash
git clone https://github.com/SAMKIT-CHOPDA/ai-voice-controlled-desktop-assistant.git
cd ai-voice-controlled-desktop-assistant
```

## 2. Create virtual environment

```bash
python -m venv .venv
```

## 3. Activate environment

```bash
.venv\Scripts\activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure API key

Create `.env` in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

**Never commit `.env` to GitHub.**

## 6. Run

```bash
python main.py
```

---

# 🗺️ Development Roadmap

## Phase 1 — Core Voice Pipeline

- [x] Microphone input
- [x] Silero voice activity detection
- [x] faster-whisper speech recognition
- [x] OpenAI text-to-speech

## Phase 2 — AI Agent

- [x] OpenAI Responses API
- [x] Function/tool calling
- [x] Automatic tool selection
- [x] Multiple tool execution
- [x] Iterative tool execution
- [x] Conversational context

## Phase 3 — Desktop Capabilities

- [x] Application control
- [x] Website opening
- [x] Web search
- [x] System monitoring
- [x] Volume control
- [x] Media control
- [x] Window control
- [x] Screenshot capture
- [x] File search
- [x] Notes
- [x] Clipboard operations

## Phase 4 — Intelligence & Productivity ✅

### Smart Research
- [x] Web research
- [x] Current information retrieval
- [x] Multi-step research

### Document Understanding
- [x] PDF reading
- [x] DOCX reading
- [x] TXT reading
- [x] Document search

### File Organization
- [x] File categorization
- [x] Preview before moving
- [x] Confirmation before execution
- [x] Duplicate filename handling

### Conversation & Memory
- [x] Multi-turn conversational context
- [x] Persistent long-term memory
- [x] Memory search
- [x] Memory deletion

### Study Assistant
- [x] Topic explanations
- [x] Practice questions
- [x] Interactive quizzes
- [x] Answer evaluation

### Writing Assistant
- [x] Writing improvement
- [x] Grammar correction
- [x] Paraphrasing
- [x] Summarization
- [x] Email generation

## Phase 5 — Advanced Desktop Agent ✅

- [x] Screen reading / visual understanding
- [x] GUI interaction
- [x] Context-aware notifications
- [x] Developer assistant
- [x] Python/package/environment management
- [x] Smart process management
- [x] Audit/request logging

## Phase 6 — Productivity Integrations

- [ ] Weather
- [ ] News and research improvements
- [ ] Timers and reminders
- [ ] Calendar integration
- [ ] Email integration
- [ ] YouTube search and control
- [ ] Scheduled system actions
- [ ] Persistent preferences
- [ ] Daily briefing

---

# 🔮 Future Improvements

- [ ] More robust multi-step reasoning
- [ ] Better error recovery
- [ ] Confirmation for sensitive computer actions
- [x] Action and conversation logging
- [ ] Graphical user interface
- [ ] Conversation history
- [ ] Visual tool/action status
- [ ] Better screen understanding
- [ ] Improved browser automation
- [ ] Interruptible speech
- [ ] Configurable assistant personality
- [ ] Improved wake-word support

---

# 📈 Current Status

**Backend — COMPLETE ✅**

The project has evolved from a basic voice-controlled desktop utility into a multi-capability AI desktop agent with desktop automation, visual understanding, system/process management, developer tooling, Python environment management, notifications, memory, productivity tools, and audit logging.

Current high-level pipeline:

```text
Voice
  ↓
Speech Recognition
  ↓
LLM Reasoning
  ↓
Tool Selection
  ↓
Python Tools
  ↓
Desktop / Web / Files / Documents
System / Processes / Memory / Study / Writing
  ↓
LLM Response
  ↓
Audit Log
  ↓
Voice Output
```

### Current Development Stage

The complete backend has been implemented and tested. The next major stage is the **graphical frontend**, which will provide a user-friendly desktop interface so the assistant can be used without the command line.

Planned frontend capabilities include:

- Chat interface
- Voice interaction controls
- Conversation history
- Assistant status indicators
- Tool/action activity display
- System information dashboard
- Settings
- Integration with the existing `ask_llm()` backend

---

# 🧪 Testing

Backend features can be tested directly through `ask_llm()` from the command line.

Example:

```bash
python -c "from assistant import ask_llm; print(ask_llm('Which process is using the most memory?'))"
```

For syntax validation:

```bash
python -m py_compile assistant.py audit_logger.py
```

The command-line interface is currently the development/test interface. A graphical interface is the next major development stage.

---

# 📄 License

This project is currently provided for educational and portfolio purposes.

A formal open-source license can be added if the project is later released for public contribution.
