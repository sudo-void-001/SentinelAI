"""
reports.py — Report generation layer for SentinelAI.

Generates daily and weekly threat intelligence reports
as text files saved to the reports/ folder.
"""

import os
from datetime import datetime, timedelta
from database import get_recent_articles, get_critical_cves


REPORTS_DIR = "reports"


def ensure_reports_dir() -> None:
    """Create reports directory if it doesn't exist."""
    os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_daily_report() -> str:
    """
    Generate a daily threat intelligence report.
    Saves to reports/daily_YYYY_MM_DD.txt

    Returns:
        File path of the generated report.
    """
    ensure_reports_dir()

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{REPORTS_DIR}/daily_{date_str}.txt"

    articles = get_recent_articles(limit=20)
    critical_cves = get_critical_cves()

    lines = []
    lines.append("=" * 60)
    lines.append(f"  SENTINELAI DAILY REPORT — {date_str}")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"  Articles Collected : {len(articles)}")
    lines.append(f"  Critical CVEs      : {len(critical_cves)}")
    lines.append(f"  Generated At       : {datetime.utcnow().strftime('%H:%M UTC')}")
    lines.append("")

    lines.append("─" * 60)
    lines.append("  TOP THREATS")
    lines.append("─" * 60)

    for i, article in enumerate(articles[:10], 1):
        severity = article.get("severity", "low").upper()
        title = article.get("title", "")
        source = article.get("source", "")
        summary = article.get("summary", "No summary yet.")
        url = article.get("url", "")

        lines.append(f"\n  {i}. [{severity}] {title}")
        lines.append(f"     Source  : {source}")
        lines.append(f"     Summary : {summary}")
        lines.append(f"     URL     : {url}")

    lines.append("")
    lines.append("─" * 60)
    lines.append("  CRITICAL CVEs (CVSS 9.0+)")
    lines.append("─" * 60)

    if critical_cves:
        for cve in critical_cves:
            lines.append(f"\n  {cve['cve_id']} — CVSS {cve['cvss_score']}")
            lines.append(f"  {cve['description'][:120]}...")
    else:
        lines.append("\n  No critical CVEs in database yet.")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  END OF REPORT — SentinelAI v1.0")
    lines.append("=" * 60)

    report_text = "\n".join(lines)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"[reports.py] Daily report saved: {filename}")
    return filename


def generate_weekly_report() -> str:
    """
    Generate a weekly summary report.
    Saves to reports/weekly_YYYY_WXX.txt

    Returns:
        File path of the generated report.
    """
    ensure_reports_dir()

    now = datetime.utcnow()
    week_num = now.strftime("%W")
    year = now.strftime("%Y")
    filename = f"{REPORTS_DIR}/weekly_{year}_W{week_num}.txt"

    articles = get_recent_articles(limit=50)
    critical_cves = get_critical_cves()

    lines = []
    lines.append("=" * 60)
    lines.append(f"  SENTINELAI WEEKLY REPORT — {year} Week {week_num}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Total Articles     : {len(articles)}")
    lines.append(f"  Critical CVEs      : {len(critical_cves)}")
    lines.append(f"  Generated At       : {now.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append("─" * 60)
    lines.append("  ALL CRITICAL CVEs THIS WEEK")
    lines.append("─" * 60)

    if critical_cves:
        for cve in critical_cves:
            lines.append(f"\n  {cve['cve_id']} — CVSS {cve['cvss_score']}")
            lines.append(f"  Exploited: {'Yes' if cve['is_exploited'] else 'No'}")
            lines.append(f"  {cve['description'][:120]}...")
    else:
        lines.append("\n  No critical CVEs recorded this week.")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  END OF REPORT — SentinelAI v1.0")
    lines.append("=" * 60)

    report_text = "\n".join(lines)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"[reports.py] Weekly report saved: {filename}")
    return filename