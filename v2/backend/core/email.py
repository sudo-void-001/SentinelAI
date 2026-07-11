"""
core/scheduler_v2.py — V2 digest scheduler.

Sends email digests to each user at their chosen slot time.
Runs as background thread inside FastAPI.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from core.config import GROQ_API_KEY, GROQ_MODEL
from core.email import send_daily_digest_email
from core.database import SessionLocal
from models.user import User


def get_v1_articles(limit: int = 10) -> list[dict]:
    """Fetch articles from V1 database."""
    v1_db = Path(__file__).resolve().parent.parent.parent.parent / "v1" / "data" / "sentinel.db"
    if not v1_db.exists():
        return []
    conn = sqlite3.connect(str(v1_db))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM articles ORDER BY created_at DESC LIMIT ?",
        (limit,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_v1_cves(limit: int = 5) -> list[dict]:
    """Fetch CVEs from V1 database."""
    v1_db = Path(__file__).resolve().parent.parent.parent.parent / "v1" / "data" / "sentinel.db"
    if not v1_db.exists():
        return []
    conn = sqlite3.connect(str(v1_db))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM cves WHERE cvss_score >= 7.0 ORDER BY cvss_score DESC LIMIT ?",
        (limit,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def send_digest_for_slot(hour: int) -> None:
    """
    Send digest email to all users assigned to this hour slot.

    Args:
        hour: IST hour to send digest for.
    """
    db = SessionLocal()
    try:
        users = db.query(User).filter(
            User.digest_slot == hour,
            User.is_active == True,
            User.notify_email == True,
        ).all()

        if not users:
            return

        articles = get_v1_articles(limit=10)
        cves = get_v1_cves(limit=5)

        for user in users:
            if user.email:
                send_daily_digest_email(
                    to_email=user.email,
                    username=user.username,
                    articles=articles,
                    cves=cves,
                )
                print(f"[scheduler_v2] Digest sent to {user.email}")
    finally:
        db.close()


def start_v2_scheduler() -> BackgroundScheduler:
    """
    Start background scheduler for all digest slots.
    Returns scheduler instance.
    """
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    # Schedule for each available IST slot
    ist_slots = [6, 7, 8, 9, 10, 11, 12]
    for hour in ist_slots:
        scheduler.add_job(
            send_digest_for_slot,
            trigger=CronTrigger(hour=hour, minute=0, timezone="Asia/Kolkata"),
            args=[hour],
            id=f"digest_slot_{hour}",
        )
        print(f"[scheduler_v2] Digest job scheduled for {hour}:00 IST")

    scheduler.start()
    print("[scheduler_v2] V2 scheduler running")
    return scheduler