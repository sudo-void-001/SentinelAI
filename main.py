"""
main.py — Entry point for SentinelAI.

Initializes the database and starts the scheduler.
This is the only file you run directly.

Usage:
    python main.py
"""

from database import initialize_database
from scheduler import start_scheduler
from utils import log


def main() -> None:
    """
    Initialize SentinelAI and start the pipeline.
    """
    print("=" * 50)
    print("  SentinelAI v1.0 — Threat Intelligence Platform")
    print("=" * 50)

    log("main", "Initializing database")
    initialize_database()

    log("main", "Starting scheduler")
    start_scheduler()


if __name__ == "__main__":
    main()