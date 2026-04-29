```
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗    ███╗   ███╗████████╗ ██████╗ ███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝    ████╗ ████║╚══██╔══╝██╔════╝ ╚════██║
     ██║███████║██████╔╝██║   ██║██║███████╗    ██╔████╔██║   ██║   ████████     ██╔╝    
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║    ██║╚██╔╝██║   ██║   ██╔═══╝██  ██╔╝    
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║    ██║ ╚═╝ ██║   ██║   ╚██████╗   ██║    
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝    ╚═╝     ╚═╝   ╚═╝    ╚═════╝   ╚═╝     
```

### **I'm not AI-powered, I'm AI-possessed. There's a difference— MT67**

*A fully autonomous, always-listening AI personal assistant.*

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini 2.5 Flash](https://img.shields.io/badge/Gemini_2.5_Flash-Native_Audio-4285F4?style=flat-square&logo=google&logoColor=white)](https://deepmind.google)
[![OpenCV](https://img.shields.io/badge/OpenCV-Camera_Vision-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org)
[![Playwright](https://img.shields.io/badge/Playwright-Browser_Control-45BA4B?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev)
[![Telegram](https://img.shields.io/badge/Telegram-Bridge-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> *"Sometimes you gotta run before you can walk."* — Tony Stark

---

## 🤖 What is JARVIS-MT67?

**JARVIS-MT67** is a fully autonomous, always-listening AI personal assistant inspired by Tony Stark's J.A.R.V.I.S. from the Iron Man universe.

While most AI assistants just answer questions, JARVIS-MT67 *acts*. It streams your voice in real-time, watches through your camera, reads your screen, controls your browser, manages your files, finds flights, plays YouTube, monitors Steam and Epic game updates, bridges your Telegram, and unmutes itself the moment it hears a clap — all from a single Python process running locally on your machine.

With **15+ deeply integrated tools**, a living **memory and personality system**, and a soul defined in markdown, JARVIS-MT67 is engineered to feel less like software and more like a presence — one that learns, adapts, and genuinely knows you over time.

---

## ✨ Features

### 🎙️ Voice & Audio

| Feature | Description |
| --- | --- |
| **Voice Streaming** | Real-time continuous listening via **Gemini 2.5 Flash Native Audio** — no push-to-talk, no delay |
| **Clap Detection** | Clap once to mute/unmute, twice to wake JARVIS, three times for... something fun |
| **Streaming TTS** | Natural voice responses streamed back in real-time using the Charon voice |
| **Text Input** | Type commands directly via the UI input bar |

### 👁️ Vision & Screen

| Feature | Description |
| --- | --- |
| **Real-Time Camera Vision** | Live webcam feed processed via **OpenCV** — JARVIS sees and describes your environment |
| **Screen Capture & Analysis** | Full desktop screenshot → Gemini vision analysis on demand |

### 🌐 Web & Browser

| Feature | Description |
| --- | --- |
| **Browser Control** | Autonomous browser automation — open tabs, click, search, navigate, fill forms via Playwright |
| **Web Search** | Real-time internet search integrated into conversation context |
| **Flight Finder** | Voice-activated flight search — *"Find me flights to Tokyo next Friday"* |
| **YouTube Control** | Search, play, summarize YouTube videos via voice |
| **Weather Reports** | Real-time weather for any city, spoken back naturally |

### 🖥️ System & Desktop

| Feature | Description |
| --- | --- |
| **Desktop Control** | Move mouse, click, type, open apps, keyboard shortcuts via voice |
| **Computer Settings** | Adjust volume, brightness, Wi-Fi, Bluetooth and system settings by voice |
| **Computer Control** | High-level system commands — shutdown, restart, lock screen, task management |
| **File Manager** | Create, move, rename, delete, and search files hands-free |
| **Dev Agent** | Build complete multi-file projects from a single voice description — plans, writes, installs, runs and fixes errors automatically |
| **Code Helper** | Generate, explain, and debug code in any language mid-conversation |
| **Screen Processor** | Capture and analyze your screen or webcam on demand |

### 🎮 Gaming

| Feature | Description |
| --- | --- |
| **Game Updater** | Monitor and trigger updates for **Steam** and **Epic Games** titles by voice |

### 📲 Communication & Utilities

| Feature | Description |
| --- | --- |
| **Telegram Bridge** | Send and receive Telegram messages through JARVIS by voice — full two-way bridge |
| **Send Message** | Send WhatsApp, Telegram and other platform messages hands-free |
| **Reminders** | Set, manage and trigger time-based reminders with voice confirmation |

### 🧠 Intelligence

| Feature | Description |
| --- | --- |
| **Multi-Step Agent** | Complex tasks broken into steps and executed across multiple tools automatically |
| **Long-Term Memory** | Structured JSON memory that persists across sessions |
| **Soul System** | Personality, identity and behavioral guidelines defined in markdown files |

---

## 🧠 Memory & Personality System

JARVIS-MT67 doesn't reset between sessions. It *remembers* — and more importantly, it has a *self*.

The memory architecture is built on a set of markdown soul files that define who JARVIS is, who you are, and what it has learned. This system makes every interaction feel continuous, personal, and increasingly intelligent over time.

### Soul Files

| File | Purpose |
| --- | --- |
| `SOUL.md` | **Personality & Values** — JARVIS's core character: tone, ethics, humor, communication style and guiding principles |
| `USER.md` | **User Profile** — Everything JARVIS knows about you: name, preferences, habits, goals and how you like to be spoken to |
| `identity.txt` | **Self Identity** — JARVIS's understanding of what it is, its purpose and its relationship to you |
| `learnings.md` | **Persistent Learning** — Things JARVIS has learned from past conversations: facts, corrections and preferences it shouldn't have to re-discover |

## 🧠 Setting Up Your Soul Files

JARVIS uses a set of markdown files to build its understanding of you and maintain its personality across sessions. After cloning the repo, set these up before running JARVIS for the first time.

### Step 1 — Rename the templates

Template files are included in the repo. Rename them to remove the `_template` suffix:
User_template.md      →  USER.md
identity_template.md  →  identity.txt
Learnings_template.md →  learnings.md
Heartbeat_template.md →  heartbeat.md

### Step 2 — Fill in USER.md

Open `USER.md` and fill in your personal details — your name, location, preferences, habits and goals. The more you fill in, the better JARVIS knows you from day one.

### Step 3 — Customize SOUL.md (optional)

`SOUL.md` defines JARVIS's personality, tone and values. The default is already tuned for a sharp, direct, Iron Man-style assistant. Edit it if you want to change how JARVIS communicates.

### Step 4 — Leave the rest empty for now

`learnings.md` and `heartbeat.md` will be updated automatically by JARVIS during conversations. You don't need to fill them in manually — just make sure the files exist.

> ⚠️ **Never commit your filled-in soul files to a public repo.** They contain your personal information. Add them to `.gitignore` if you fork this project.

### Long-Term Structured Memory (`/memory/`)

Beyond the soul files, JARVIS maintains a `memory/` folder of structured JSON files for long-term factual storage — automatically updated during conversations via the `save_memory` tool.

---

## 🔒 Security & Disclaimer

> ⚠️ **READ THIS BEFORE RUNNING JARVIS-MT67**

JARVIS-MT67 grants an AI model direct access to your computer — including the ability to:

- Execute terminal commands and run scripts
- Control your mouse, keyboard and screen
- Read, write, move and delete files
- Open and control web browsers
- Send messages on your behalf
- Modify system settings

**This is powerful and intentionally so — but it comes with real risk.**

- The AI's judgment can be flawed or misled by ambiguous instructions
- Always supervise JARVIS when running complex multi-step tasks
- Never run JARVIS with elevated/admin privileges unless you understand what you're doing
- Keep your Gemini API key private and never commit it to any repository
- The authors accept no responsibility for data loss, system instability or unintended actions caused by this software
- also using a venv is highly recommended

**Use it on your own machine, at your own risk, with your eyes open.**


---

## 🚀 Installation

### Prerequisites

- Python 3.11 or 3.12
- A microphone
- Windows 10/11 (most system control features are Windows-only)
- A free [Gemini API key](https://aistudio.google.com/app/apikey)

### Step 1 — Clone the repository

```bash
git clone https://github.com/843subhanshkv42021-lab/Jarvis-MT67.git
cd Jarvis-MT67
```

### Step 2 — Create a virtual environment

```bash
python -m venv jarvis_env
jarvis_env\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Install Playwright browsers

```bash
playwright install
```

### Step 5 — Set up your config

A template config file is included in the repo. Rename it and fill in your API key:

```bash
# In the config/ folder, rename:
api_keys_template.json  →  api_keys.json
```

Then open `config/api_keys.json` and fill in your details:

```json
{
    "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE",
    "os_system": "windows"
}
```

You can get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com/app/apikey).

### Step 6 — Launch JARVIS

```bash
python main.py
```

On first launch, JARVIS will open a setup window where you can enter your API key and select your OS. After that it boots automatically every time.

---

## 📲 Telegram Bridge Setup

JARVIS can send and receive Telegram messages via your own personal bot — fully two-way.

### Step 1 — Create your Telegram bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts to name your bot
4. BotFather will give you a token like `7xxxxxxxxx:AAF...` — copy it

### Step 2 — Get your User ID

1. Search **@userinfobot** on Telegram
2. Send any message
3. It will reply with your numeric User ID

### Step 3 — Configure telegram\_bot.py

Open `telegram_bot.py` and fill in your credentials:

```python
BOT_TOKEN = "your_bot_token_here"
ALLOWED_USER = your_user_id_here  # just the number, no quotes
```

### Step 4 — Run the Telegram bridge

The Telegram bot runs as a separate process alongside JARVIS. Open a second terminal and run:

```bash
jarvis_env\Scripts\activate
python telegram_bot.py
```

Keep both terminals running — JARVIS in one, the Telegram bot in the other.

### Step 5 — Test it

Send a message to your bot on Telegram and JARVIS will respond. You can also tell JARVIS by voice to send you a Telegram message and it will push it to your phone.

---

## 📁 Project Structure

```
Jarvis-MT67/
├── main.py                    # Entry point — boots JARVIS
├── ui.py                      # Desktop overlay UI (tkinter, animated rings + orb)
├── requirements.txt           # Python dependencies
├── setup.py                   # Setup script
├── telegram_bot.py            # Telegram bridge bot (run separately)
├── jarvis_telegram_patch.py   # Telegram inbox/outbox handler
├── SOUL.md                    # JARVIS personality & values
├── USER.md                    # User profile
├── identity.txt               # JARVIS self-identity
├── learnings.md               # Persistent learning file
├── actions/                   # Tool implementations
│   ├── browser_control.py     # Playwright browser automation
│   ├── file_controller.py     # File system operations
│   ├── screen_processor.py    # Camera & screen vision
│   ├── dev_agent.py           # Project builder agent
│   ├── code_helper.py         # Code generation & execution
│   ├── computer_control.py    # Mouse, keyboard, system
│   ├── computer_settings.py   # System settings
│   ├── desktop.py             # Desktop control
│   ├── flight_finder.py       # Flight search
│   ├── game_updater.py        # Steam & Epic Games
│   ├── open_app.py            # App launcher
│   ├── reminder.py            # Reminders
│   ├── send_message.py        # Messaging
│   ├── weather_report.py      # Weather
│   ├── web_search.py          # Web search
│   └── youtube_video.py       # YouTube control
├── agent/                     # Multi-step agent system
│   ├── executor.py            # Task executor
│   ├── planner.py             # Task planner
│   ├── error_handler.py       # Error recovery
│   └── task_queue.py          # Task queue manager
├── core/                      # Core system files
├── memory/                    # Long-term structured JSON memory
└── config/                    # API keys & settings (NOT in repo — create your own)
    └── api_keys_template.json # Template — rename to api_keys.json and fill in
```

---

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| **Language** | Python 3.11+ |
| **AI Model** | Google Gemini 2.5 Flash — Native Audio (Live API) |
| **Vision** | OpenCV (`cv2`) — real-time camera processing |
| **Audio I/O** | `sounddevice` — low-latency microphone streaming |
| **UI** | `tkinter` — animated desktop overlay with rings, orb and waveform |
| **Browser Automation** | Playwright |
| **Telegram** | `python-telegram-bot` |
| **Screen Capture** | `mss` + `Pillow` |
| **System Control** | `pyautogui`, `pywinauto`, `pycaw`, `comtypes` |
| **Clap Detection** | `sounddevice` + `numpy` — frequency analysis based |

---

## 🙏 Acknowledgements

Some foundational files and structural patterns were taken from the open-source project **[Jarvis-MK37]** by FatihMakes — an incredible project by an 18-year-old developer building toward Mark 85. MT67 extends and rebuilds on top of that foundation with new tools, deeper memory, clap detection, live camera vision, flight search, game management, a completely redesigned UI and much more. Go give it a ⭐ too.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*"I am JARVIS. I am always here."*

⭐ **Star this repo if you want to see MT68.**