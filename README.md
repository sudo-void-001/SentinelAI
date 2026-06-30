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

# Screenshots

## Terminal Execution

![Terminal Output]

<img width="3840" height="2160" alt="Screenshot 2026-06-30 150212" src="https://github.com/user-attachments/assets/c6abf6bb-d5de-42cc-8077-7db544dab89e" />


*SentinelAI running successfully with scheduler, database, news collection, CVE tracking, AI summarization, and Telegram integration.*

---

## Telegram Digest — Part 1

![Telegram Digest Part 1]
<img width="576" height="1280" alt="telegram(1)" src="https://github.com/user-attachments/assets/f3f3f139-f27b-454e-887b-79be0ab48bca" />


*Daily cybersecurity digest showing threat summaries and article intelligence.*

---

## Telegram Digest — Part 2

![Telegram Digest Part 2]
<img width="576" height="1280" alt="telegram(2)" src="https://github.com/user-attachments/assets/08f2a1b4-91bd-4954-bdc7-35129e765f73" />


*Continuation of the Telegram digest with additional threat reports and AI-generated summaries.*

---
