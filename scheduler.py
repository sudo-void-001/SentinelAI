"""
scheduler.py — Automated pipeline scheduler for SentinelAI.

Uses APScheduler to run the full pipeline on a schedule.
News and CVEs collected every 6 hours.
Daily report and Telegram digest sent at 09:00 IST (03:30 UTC).
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from config import SCHEDULE_INTERVAL_HOURS
from utils import log


scheduler = BlockingScheduler(timezone="UTC")


def run_collection_pipeline() -> None:
    """
    Run full data collection and AI enrichment pipeline.
    Fetches news, CVEs, summarizes with AI, stores in DB.
    """
    from news import collect_all_news
    from cve import collect_all_cves
    from database import insert_article, insert_cve
    from ai import enrich_article

    log("scheduler", "Starting collection pipeline")

    # Collect and store news
    articles = collect_all_news()
    for article in articles:
        enriched = enrich_article(article.title, article.raw_content or "")
        article.summary = enriched["summary"]
        article.category = enriched["category"]
        article.severity = enriched["severity"]
        insert_article(article)

    log("scheduler", f"Stored {len(articles)} articles")

    # Collect and store CVEs
    cves = collect_all_cves()
    for cve in cves:
        insert_cve(cve)

    log("scheduler", f"Stored {len(cves)} CVEs")


def run_daily_report() -> None:
    """
    Generate daily report and send Telegram digest.
    Runs at 09:00 IST (03:30 UTC) every day.
    """
    from reports import generate_daily_report
    from database import get_recent_articles, get_critical_cves
    from telegram_bot import send_daily_digest, send_critical_alert

    log("scheduler", "Generating daily report")
    generate_daily_report()

    articles = get_recent_articles(limit=5)
    send_daily_digest(articles)

    critical_cves = get_critical_cves()
    for cve in critical_cves[:3]:
        send_critical_alert(cve)

    log("scheduler", "Daily report and alerts sent")


def start_scheduler() -> None:
    """
    Register all jobs and start the blocking scheduler.
    This function never returns — runs until interrupted.
    """
    scheduler.add_job(
        run_collection_pipeline,
        trigger="interval",
        hours=SCHEDULE_INTERVAL_HOURS,
        next_run_time=datetime.utcnow(),
        id="collection_pipeline",
    )

    scheduler.add_job(
        run_daily_report,
        trigger=CronTrigger(hour=3, minute=30),  # 03:30 UTC = 09:00 IST
        id="daily_report",
    )

    log("scheduler", f"Pipeline runs every {SCHEDULE_INTERVAL_HOURS} hours")
    log("scheduler", "Daily report runs at 09:00 IST (03:30 UTC)")
    log("scheduler", "SentinelAI is running. Press Ctrl+C to stop.")

    scheduler.start()