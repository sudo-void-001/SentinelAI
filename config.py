"""
config.py — Central configuration for SentinelAI.

All settings and secrets are loaded here from .env.
Every other module imports from this file.
Never read .env directly in any other module.
"""

import os
from .env import load_dotenv

# Load .env file into environment
load_dotenv()

# ─── AI ───────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = "llama3-8b-8192"

# ─── TELEGRAM ─────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

# ─── DATABASE ─────────────────────────────────────
DB_PATH: str = "data/sentinel.db"

# ─── COLLECTION LIMITS ────────────────────────────
NEWS_FETCH_LIMIT: int = int(os.getenv("NEWS_FETCH_LIMIT", "50"))
CVE_FETCH_LIMIT: int = int(os.getenv("CVE_FETCH_LIMIT", "20"))

# ─── SCHEDULER ────────────────────────────────────
SCHEDULE_INTERVAL_HOURS: int = int(os.getenv("SCHEDULE_INTERVAL_HOURS", "6"))

# ─── NEWS SOURCES ─────────────────────────────────
HACKERNEWS_API_URL: str = "https://hn.algolia.com/api/v1/search"
NVD_API_URL: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"
CISA_KEV_URL: str = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

RSS_FEEDS: list[str] = [
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews",
]