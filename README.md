# SentinelAI

> AI-powered Cyber Threat Intelligence Platform

SentinelAI automatically collects cybersecurity news, tracks CVEs,
summarizes threats using AI, and delivers daily intelligence reports
via Telegram — so you spend less time searching and more time acting.

---

## Features

- Automated cybersecurity news collection from 4 sources
- CVE tracking via NVD and CISA Known Exploited Vulnerabilities
- AI-powered summarization using Groq (llama3-8b)
- Daily and weekly threat reports
- Telegram alerts for critical CVEs
- Fully local — your data never leaves your machine

---

## Tech Stack

| Layer        | Technology        |
|--------------|-------------------|
| Language     | Python 3.11+      |
| Database     | SQLite            |
| AI           | Groq API          |
| Scheduler    | APScheduler       |
| Notifications| Telegram Bot API  |

---

## Quick Start

```bash
git clone https://github.com/sudo-void-001/SentinelAI.git
cd SentinelAI
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py