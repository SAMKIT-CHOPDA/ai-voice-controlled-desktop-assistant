# 🎙️ AI Voice-Controlled Desktop Assistant

> **A tool-using AI voice assistant for Windows that combines speech recognition, hierarchical JEV routing, adaptive LLM selection, and Python-based desktop automation.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-OpenAI-412991?logo=openai&logoColor=white)
![Speech](https://img.shields.io/badge/Speech-Faster--Whisper-orange)
![Architecture](https://img.shields.io/badge/Architecture-JEV%20%2B%20Adaptive%20Routing-purple)
![Status](https://img.shields.io/badge/Status-Frozen-success)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 🚀 What is this?

This project is a **Python-based AI voice-controlled desktop assistant for Windows**.

The assistant listens to natural voice requests, converts speech to text using Faster-Whisper, classifies the request through a two-level JEV routing architecture, and either executes a deterministic Python tool or selects an appropriate LLM for a general request.

The project is designed around one central idea:

> **Use deterministic tools whenever the task is known, and use the minimum capable LLM level when reasoning is required.**

This creates a practical AI-agent architecture that combines speech processing, intelligent routing, LLM reasoning, function calling, and computer interaction.

---

## 🧠 Core Architecture

The final frozen architecture is:

```text
┌──────────────────────┐
│      Microphone      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      Silero VAD      │
│ Speech Detection     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│    Faster-Whisper    │
│    Speech-to-Text    │
└──────────┬───────────┘
           ↓
┌──────────────────────────────┐
│        JEV Level 1           │
│ Request / Intent Routing     │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ↓                ↓
 DIRECT TOOL       GENERAL_LLM
       │                │
       │                ↓
       │        ┌─────────────────────┐
       │        │    JEV Level 2      │
       │        │   Model Router      │
       │        └─────────┬───────────┘
       │                  │
       │        ┌─────────┼─────────┐
       │        ↓         ↓         ↓
       │      FAST     STANDARD    DEEP
       │        │         │         │
       │        ↓         ↓         ↓
       │      Luna      Terra       Sol
       │
       └──────────────┬──────────────┘
                      ↓
              Final Response
                      ↓
                OpenAI TTS
                      ↓
                  Speaker
```

### JEV Level 1 — Task Routing

JEV Level 1 determines whether a request can be handled by a deterministic local tool or requires general LLM reasoning.

```text
User Request
     ↓
JEV Level 1
     ├── DIRECT TOOL → execute Python tool → return result
     │
     └── GENERAL_LLM → continue to JEV Level 2
```

Direct commands can therefore bypass unnecessary LLM generation.

### JEV Level 2 — Adaptive Model Routing

Only `GENERAL_LLM` requests reach Level 2.

The router selects the minimum model level expected to satisfy the request:

| Level | Model | Reasoning | Intended Use |
|---|---|---|---|
| **FAST** | GPT-5.6 Luna | `none` | Simple factual and conversational requests |
| **STANDARD** | GPT-5.6 Terra | `low` | Normal explanations, instructions and writing |
| **DEEP** | GPT-5.6 Sol | `medium` | Analysis, debugging, research and complex reasoning |

This avoids using the deepest reasoning model for every request and provides an adaptive latency/capability trade-off.

---

## ✨ Key Features

### 🎙️ Voice Interface

- Microphone input using SoundDevice
- Silero VAD for speech detection
- Faster-Whisper speech recognition
- Automatic speech-end detection
- Voice responses through TTS
- Optimized Whisper configuration for CPU inference

### 🧠 Hierarchical AI Routing

- JEV Level 1 deterministic task routing
- JEV Level 2 adaptive model routing
- FAST / STANDARD / DEEP model levels
- Model-specific reasoning effort
- Direct tool execution without unnecessary LLM calls
- Concise voice-response behavior

### 🤖 LLM Agent

- OpenAI Responses API
- Structured function/tool calling
- Automatic tool selection
- Iterative tool execution
- Multi-turn conversational context
- Tool-result grounding before final responses

### 🖥️ Desktop Automation

- Open applications and websites
- Open folders
- Mouse movement and clicking
- Double-clicking
- Keyboard input, keys and hotkeys
- Scrolling and drag operations
- Window controls
- Screenshots
- Screen reading / visual understanding
- Volume and media control

### 🌐 Research & Information

- Web search
- Current web research
- Multi-step research
- Current system information

### 📄 Documents & Files

- PDF reading
- DOCX reading
- TXT reading
- Document search
- File search
- File categorization
- Preview-before-move workflow
- Explicit confirmation before moving files
- Duplicate filename handling

### 🧠 Memory & Productivity

- Persistent local memory
- Save, search, read and delete memories
- Notes
- Clipboard operations
- Calculator
- Date and time

### 📚 Study & Writing

- Topic explanations
- Practice questions
- Interactive quizzes
- Answer evaluation
- Writing improvement
- Grammar correction
- Paraphrasing
- Summarization
- Email generation

### ⚙️ System & Process Management

- Battery status
- CPU usage
- RAM usage
- Disk usage
- Wi-Fi status
- Screen resolution
- General system information
- Running-process inspection
- CPU/memory process analysis
- Process closing and restarting
- Context-aware notifications

### 👨‍💻 Developer & Python Tools

- Inspect project structure
- Read and search project files
- Modify project files when explicitly requested
- Run Python files and commands
- Git status/diff inspection
- Python environment information
- Installed package inspection
- Package availability checks
- Requirements generation and verification

### 🛡️ Reliability & Safety

- Emergency STOP mechanism
- Local JSONL audit logging
- Session identifiers
- Processing-duration logging
- Secret-pattern sanitization
- `.env` protection
- Protected project areas
- Explicit confirmation for file-organization actions

---

## 🔄 How a Request Is Processed

For a simple request such as:

> **"What is RAG in AI?"**

The request follows this path:

```text
Voice
 ↓
Silero VAD
 ↓
Faster-Whisper
 ↓
JEV Level 1
 ↓
GENERAL_LLM
 ↓
JEV Level 2
 ↓
FAST
 ↓
GPT-5.6 Luna
 ↓
Concise Response
 ↓
TTS
```

For a deterministic request such as:

> **"Play the first video in Jojo ASMR."**

The request can be handled directly:

```text
Voice
 ↓
Silero VAD
 ↓
Faster-Whisper
 ↓
JEV Level 1
 ↓
YOUTUBE_PLAY
 ↓
Python Tool
 ↓
Result
 ↓
TTS
```

For a complex request such as:

> **"Compare RAG and fine-tuning and explain their main trade-offs."**

JEV Level 2 routes the request to the deeper reasoning level:

```text
Voice
 ↓
Faster-Whisper
 ↓
JEV Level 1
 ↓
GENERAL_LLM
 ↓
JEV Level 2
 ↓
DEEP
 ↓
GPT-5.6 Sol + medium reasoning
 ↓
Concise Response
 ↓
TTS
```

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| **Python** | Core application |
| **OpenAI Responses API** | LLM reasoning and tool calling |
| **GPT-5.6 Luna** | Fast model level |
| **GPT-5.6 Terra** | Standard model level |
| **GPT-5.6 Sol** | Deep reasoning model level |
| **Faster-Whisper** | Speech recognition |
| **Silero VAD** | Voice activity detection |
| **SoundDevice** | Microphone and audio I/O |
| **OpenAI TTS** | Voice output |
| **PyAutoGUI** | Desktop automation |
| **Pyperclip** | Clipboard operations |
| **psutil** | System/process monitoring |
| **PyMuPDF** | PDF extraction |
| **python-docx** | DOCX extraction |
| **python-dotenv** | Environment configuration |
| **Winotify** | Windows notifications |

---

## 📂 Project Structure

```text
Ai-assistant-voice-controlled/
│
├── main.py                     # Main voice-assistant loop
├── assistant.py                # LLM + JEV integration + tool loop
├── jev.py                      # JEV Level 1 routing
├── model_router.py             # JEV Level 2 model routing
├── tools.py                    # Core deterministic tools
├── wake_word.py                # VAD + Faster-Whisper voice input
├── tts.py                      # Voice output
│
├── gui_tools.py                # GUI interaction tools
├── screen_tools.py             # Screen/screenshot tools
├── document_tools.py           # Document processing
├── file_organization_tools.py  # File organization
├── memory_tools.py             # Local memory
├── study_tools.py              # Study utilities
├── writing_tools.py             # Writing utilities
├── notification_tools.py       # Notifications
├── developer_tools.py          # Developer utilities
├── environment_tools.py        # Environment information
├── process_tools.py            # Process management
├── audit_logger.py             # Audit logging
│
├── benchmark_models.py         # LLM model benchmark
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env                        # Local only — never commit
```

---

## 🎯 Example Commands

The assistant accepts natural language rather than requiring rigid command syntax.

### 🖥️ Desktop

```text
"Open Chrome."
"Open YouTube and search for Jojo's ASMR."
"Open my Downloads folder."
"Take a screenshot."
"Minimize the current window."
"Turn the volume up."
"Pause the media."
```

### 📊 System

```text
"What is my battery percentage?"
"How much RAM am I using?"
"How much CPU am I using?"
"How much free storage do I have?"
"Is my internet working?"
```

### 📁 Files & Documents

```text
"Find my resume."
"Read my project report."
"Summarize this PDF."
"Organize my Downloads folder."
"Show me what files would be organized."
```

### 📚 Study

```text
"Explain neural networks at a beginner level."
"Give me practice questions about machine learning."
"Quiz me on Python OOP."
"Evaluate my answer."
```

### ✍️ Writing

```text
"Improve this paragraph formally."
"Correct my grammar."
"Paraphrase this paragraph."
"Summarize this text."
"Write a professional email."
```

---

## 🔐 Security & Safety

Because this assistant can interact with the local computer, security is an important part of the design.

- API credentials are stored in `.env`
- `.env`, `.venv` and logs are excluded from Git
- Calculator expressions use a restricted AST-based parser
- Desktop actions are exposed through explicit tools
- File organization uses preview and confirmation
- Arbitrary Python execution is not exposed as a normal LLM tool
- Developer tools are restricted to the project directory
- Protected areas such as `.env`, `.git` and `.venv` are guarded
- Package installation/removal/upgrades require explicit requests
- Audit logs sanitize common secret patterns
- An emergency STOP mechanism can stop the tool-execution loop

> ⚠️ **Important:** This assistant can control parts of a Windows computer. Run it only in an environment where you understand and trust the actions being requested.

---

## 🚀 Installation

### Prerequisites

- Windows
- Python 3.x
- Working microphone
- Speakers or headphones
- OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/SAMKIT-CHOPDA/ai-voice-controlled-desktop-assistant.git
cd ai-voice-controlled-desktop-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the API key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
TYPESAFE_API_KEY=your_api_key_here
```

Never commit your `.env` file to GitHub.

### 6. Run the assistant

```bash
python main.py
```

---

## 🧪 Testing

### Model router tests

The JEV Level 2 router can be tested independently:

```bash
python test_model_router.py
```

The tests verify routing of representative FAST, STANDARD and DEEP requests.

### Python syntax validation

```bash
python -m py_compile assistant.py
python -m py_compile model_router.py
```

### Direct assistant test

```bash
python -c "from assistant import ask_llm; print(ask_llm('What is RAG in AI?'))"
```

### Model benchmark

The project also includes a benchmark script for comparing the configured model levels:

```bash
python benchmark_models.py
```

---

## 📊 Model Routing Benchmark

The implemented model router was benchmarked using representative FAST, STANDARD and DEEP queries.

Observed benchmark results during development:

| Level | Model | Avg. First Token | Avg. Total Time |
|---|---|---:|---:|
| FAST | GPT-5.6 Luna | ~1.73 s | ~4.64 s |
| STANDARD | GPT-5.6 Terra | ~1.39 s | ~9.17 s |
| DEEP | GPT-5.6 Sol | ~1.58 s | ~6.04 s |

These measurements are **development-time observations**, not fixed guarantees. API latency can vary with network conditions, workload, model availability and response length.

---

## 🧭 Project Development Journey

```text
Basic Voice Commands
        ↓
Voice + Speech Recognition
        ↓
LLM Integration
        ↓
Function / Tool Calling
        ↓
Desktop Automation
        ↓
Documents & File Management
        ↓
Memory & Productivity
        ↓
Study & Writing Assistance
        ↓
Screen Understanding & GUI Control
        ↓
Developer & System Tools
        ↓
Audit Logging & Safety
        ↓
JEV Level 1 Routing
        ↓
JEV Level 2 Adaptive Model Routing
        ↓
Response-Length Optimization
        ↓
🔒 FROZEN CORE ARCHITECTURE
```

---

## 🔒 Frozen Project Version

The current architecture is intentionally **frozen** as a stable project baseline.

The frozen core includes:

- Silero VAD
- Faster-Whisper speech recognition
- JEV Level 1 deterministic/general routing
- JEV Level 2 adaptive model routing
- FAST / STANDARD / DEEP model selection
- GPT-5.6 Luna / Terra / Sol model mapping
- Model-specific reasoning effort
- OpenAI Responses API integration
- Python tool execution
- Concise voice-response behavior
- Current TTS integration

Further experiments or optimizations should be treated as separate branches/phases rather than modifying the frozen core unnecessarily.

---

## 🎓 What This Project Demonstrates

This project brings together several areas of modern AI and software engineering:

- **Speech processing**
- **Natural language understanding**
- **LLM-based reasoning**
- **Hierarchical AI-agent routing**
- **Adaptive model selection**
- **Function/tool calling**
- **Computer-use automation**
- **Document processing**
- **File-system interaction**
- **Persistent memory**
- **System monitoring**
- **Process management**
- **Developer tooling**
- **Security-conscious logging**
- **Modular Python application design**

The main architectural contribution of the project is the separation between **task routing** and **model routing**:

```text
JEV Level 1
     ↓
What kind of task is this?
     ↓
DIRECT TOOL / GENERAL_LLM
     ↓
JEV Level 2
     ↓
How much reasoning does this request need?
     ↓
FAST / STANDARD / DEEP
```

This allows the assistant to avoid unnecessary LLM reasoning for deterministic operations while adapting model capability to the complexity of general requests.

---

<p align="center">

### 🎙️ Built as a practical hierarchical AI agent for the Windows desktop

**Project Status: 🔒 FROZEN / COMPLETED**

</p>
