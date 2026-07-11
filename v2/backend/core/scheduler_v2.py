"""
core/scheduler_v2.py — V2 email digest scheduler.
Sends digest emails to users at their chosen IST slot.
"""

import sqlite3
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def get_v1_articles(limit: int = 10) -> list:
    """Fetch articles from V1 SQLite database."""
    v1_db = (
        Path(__file__).resolve()
        .parent.parent.parent.parent
        / "v1" / "data" / "sentinel.db"
    )
    if not v1_db.exists():
        print(f"[scheduler_v2] V1 database not found at {v1_db}")
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


def get_v1_cves(limit: int = 5) -> list:
    """Fetch CVEs from V1 SQLite database."""
    v1_db = (
        Path(__file__).resolve()
        .parent.parent.parent.parent
        / "v1" / "data" / "sentinel.db"
    )
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
        hour: IST hour (6-12) to send digest for.
    """
    from core.database import SessionLocal
    from core.email import send_daily_digest_email
    from models.user import User

    db = SessionLocal()
    try:
        users = db.query(User).filter(
            User.digest_slot == hour,
            User.is_active == True,
            User.notify_email == True,
        ).all()

        if not users:
            print(f"[scheduler_v2] No users for slot {hour}:00")
            return

        articles = get_v1_articles(limit=10)
        cves = get_v1_cves(limit=5)

        for user in users:
            if user.email:
                try:
                    send_daily_digest_email(
                        to_email=user.email,
                        username=user.username,
                        articles=articles,
                        cves=cves,
                    )
                    print(f"[scheduler_v2] Digest sent to {user.email}")
                except Exception as e:
                    print(f"[scheduler_v2] Failed to send to {user.email}: {e}")
    finally:
        db.close()


def start_v2_scheduler() -> BackgroundScheduler:
    """
    Register digest jobs for all IST slots and start scheduler.

    Returns:
        Running BackgroundScheduler instance.
    """
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    ist_slots = [6, 7, 8, 9, 10, 11, 12]
    for hour in ist_slots:
        scheduler.add_job(
            send_digest_for_slot,
            trigger=CronTrigger(
                hour=hour,
                minute=0,
                timezone="Asia/Kolkata"
            ),
            args=[hour],
            id=f"digest_slot_{hour}",
            replace_existing=True,
        )
        print(f"[scheduler_v2] Slot {hour}:00 IST registered")

    scheduler.start()
    print("[scheduler_v2] V2 scheduler started")
    return scheduler