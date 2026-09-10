# 🎙️ AI Voice-Controlled Desktop Assistant

> **A tool-using AI agent for Windows that listens to natural voice commands, reasons about the task, and interacts with the desktop through Python tools.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-OpenAI-412991?logo=openai&logoColor=white)
![Speech](https://img.shields.io/badge/Speech-Faster--Whisper-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 🚀 What is this?

This project is a **Python-based AI desktop assistant for Windows**.

Instead of relying on a fixed list of voice commands, the assistant sends each transcribed request to an LLM. The model decides whether it can answer directly or needs to call one or more tools to complete the task.

That makes the system a practical example of an **AI agent with tool calling and computer-control capabilities**.

### The core idea

```text
🎤 Speak
   ↓
🗣️ Voice Activity Detection
   ↓
📝 Speech-to-Text
   ↓
🧠 LLM Reasoning
   ↓
🛠️ Tool Selection
   ↓
💻 Python Tool Execution
   ↓
🤖 Final Response
   ↓
🔊 Text-to-Speech
```

---

## ✨ Highlights

### 🎙️ Voice Interface
- Microphone input
- Silero VAD for speech detection
- Faster-Whisper speech recognition
- Automatic utterance-end detection
- OpenAI TTS voice responses

### 🧠 AI Agent
- OpenAI Responses API
- Structured function/tool calling
- Automatic tool selection
- Multiple and iterative tool calls
- Multi-turn conversational context

### 🖥️ Desktop Automation
- Open applications and websites
- Open folders
- Mouse movement and clicking
- Double-clicking
- Keyboard input, keys and hotkeys
- Scrolling and drag operations
- Window controls
- Screen reading / visual understanding
- Screenshots
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

### 🛑 Reliability & Security
- Emergency STOP mechanism
- Local JSONL audit logging
- Session identifiers
- Processing-duration logging
- Secret-pattern sanitization
- `.env` protection
- Protected project areas
- Explicit confirmation for file-organization actions

---

## 🏗️ Architecture

```text
┌──────────────────────┐
│      Microphone      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      Silero VAD      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Faster-Whisper     │
│   Speech-to-Text     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│     OpenAI LLM       │
│    Agent Reasoning   │
└──────────┬───────────┘
           ↓
     ┌─────┴─────┐
     ↓           ↓
 Direct      Tool Calling
 Answer          │
                 ↓
┌────────────────────────────────┐
│ Python Tool Layer               │
│                                │
│ Desktop │ Web │ Files          │
│ System  │ Docs │ Memory        │
│ Study   │ Writing │ Developer  │
└────────────────┬───────────────┘
                 ↓
            Tool Result
                 ↓
            OpenAI LLM
                 ↓
            Final Response
                 ↓
          OpenAI TTS
                 ↓
              Speaker
```

---

## 🧩 How the Agent Works

A request such as:

> **"How much RAM am I using?"**

passes through the following process:

```text
User Speech
    ↓
Speech-to-Text
    ↓
LLM receives request + available tools
    ↓
LLM selects memory_usage()
    ↓
Python executes the function
    ↓
Tool result is returned to the LLM
    ↓
LLM generates the final response
    ↓
Text-to-Speech
```

For multi-step requests, the agent can continue calling tools until the requested task is completed or no additional tool is required.

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| **Python** | Core application |
| **OpenAI Responses API** | LLM reasoning & tool calling |
| **OpenAI TTS** | Voice output |
| **Faster-Whisper** | Speech recognition |
| **Silero VAD** | Voice activity detection |
| **SoundDevice** | Microphone input |
| **PyAutoGUI** | Desktop automation |
| **Pyperclip** | Clipboard operations |
| **psutil** | System/process monitoring |
| **PyMuPDF** | PDF extraction |
| **python-docx** | DOCX extraction |
| **playsound3** | Audio playback |
| **python-dotenv** | Environment configuration |
| **Winotify** | Windows notifications |

---

## 📂 Project Structure

```text
Ai-assistant-voice-controlled/
│
├── main.py
├── assistant.py
├── tools.py
├── wake_word.py
├── tts.py
├── gui_tools.py
├── screen_tools.py
│
├── document_tools.py
├── file_organization_tools.py
├── memory_tools.py
├── study_tools.py
├── writing_tools.py
├── notification_tools.py
├── developer_tools.py
├── environment_tools.py
├── process_tools.py
├── audit_logger.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env                  # Local only — never commit
```

---

## 🎯 Example Commands

The assistant is designed for natural language rather than rigid command syntax.

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
```

**Never commit your `.env` file to GitHub.**

### 6. Run the assistant

```bash
python main.py
```

---

## 🧪 Testing

The backend can also be tested directly through the assistant's LLM interface.

Example:

```bash
python -c "from assistant import ask_llm; print(ask_llm('Which process is using the most memory?'))"
```

For Python syntax validation:

```bash
python -m py_compile assistant.py audit_logger.py
```

---

## 📈 Project Journey

The project evolved through several stages:

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
        ✅ COMPLETED
```

---

## ✅ Project Status

### **COMPLETED**

The backend has been implemented as a multi-capability AI desktop agent combining:

**Speech Processing + LLM Reasoning + Function Calling + Computer Automation**

The final application is operated through the command line and provides the complete core assistant experience without requiring a graphical frontend.

---

## 🎓 What This Project Demonstrates

This project brings together several areas of modern AI and software engineering:

- **Speech processing**
- **Natural language understanding**
- **LLM-based reasoning**
- **AI agent architecture**
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

It demonstrates how an LLM can move beyond generating text and become the reasoning layer of a practical software agent.

---

## 📄 License

This project is provided for **educational and portfolio purposes**.

A formal open-source license can be added if the project is later released for public contribution.

---

<p align="center">

### 🎙️ Built as a practical AI agent for the Windows desktop

**Project Status: ✅ COMPLETE**

</p>
