"""
main.py — Entry point for SentinelAI V1.

Run normally:        python main.py
Run once and exit:   python main.py --once
"""

import sys
from database import initialize_database
from scheduler import start_scheduler, run_collection_pipeline, run_daily_report
from utils import log


def main() -> None:
    """Initialize SentinelAI and start the pipeline."""
    print("=" * 50)
    print("  SentinelAI v1.0 — Threat Intelligence Platform")
    print("=" * 50)

    log("main", "Initializing database")
    initialize_database()

    # --once flag: run pipeline once and exit (for GitHub Actions)
    if "--once" in sys.argv:
        log("main", "Running single pipeline execution")
        run_collection_pipeline()
        run_daily_report()
        log("main", "Pipeline complete. Exiting.")
        return

    log("main", "Starting scheduler")
    start_scheduler()


if __name__ == "__main__":
    main()