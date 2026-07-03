"""
core/config.py — Central configuration for SentinelAI V2.
All settings loaded from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── APP ──────────────────────────────────────────
APP_NAME: str = "SentinelAI V2"
APP_VERSION: str = "2.0.0"
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

# ─── DATABASE ─────────────────────────────────────
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/sentinelai_v2.db"
)

# ─── JWT AUTH ─────────────────────────────────────
SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

# ─── AI ───────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = "openai/gpt-oss-20b"

# ─── EMAIL ────────────────────────────────────────
EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME", "SentinelAI")
DASHBOARD_URL: str = os.getenv("DASHBOARD_URL", "http://localhost:8501")

# ─── TELEGRAM (OPTIONAL) ──────────────────────────
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

# ─── DIGEST SLOTS (IST) ───────────────────────────
AVAILABLE_DIGEST_SLOTS: list[int] = [6, 7, 8, 9, 10, 11, 12]
DEFAULT_DIGEST_SLOT: int = 9
MAX_USERS_PER_SLOT: int = 1