"""
telegram_bot.py — Telegram notification layer for SentinelAI.

Sends daily digests and critical CVE alerts via Telegram Bot API.
Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env
"""

import requests
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_message(text: str) -> bool:
    """
    Send a plain text message to Telegram chat.

    Args:
        text: Message content to send.

    Returns:
        True if sent successfully, False otherwise.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[telegram_bot.py] Missing token or chat ID in .env")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True

    except requests.RequestException as e:
        print(f"[telegram_bot.py] Send failed: {e}")
        return False


def send_daily_digest(articles: list[dict]) -> bool:
    """
    Send top 5 articles as daily digest message with stats header.

    Args:
        articles: List of article dicts from database.

    Returns:
        True if sent successfully, False otherwise.
    """
    if not articles:
        return False

    from utils import get_severity_emoji

    date_str = datetime.utcnow().strftime("%B %d, %Y")

    # Count severities for header stats
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for article in articles:
        sev = article.get("severity", "low").lower()
        if sev in counts:
            counts[sev] += 1

    lines = [
        f"<b>🛡 SentinelAI Daily Digest</b>",
        f"<i>{date_str}</i>\n",
        f"🔴 Critical: {counts['critical']}  🟠 High: {counts['high']}  "
        f"🟡 Medium: {counts['medium']}  🟢 Low: {counts['low']}",
        f"<i>Total Articles: {len(articles)}</i>\n",
        "─" * 30,
    ]

    for i, article in enumerate(articles[:5], 1):
        severity = article.get("severity", "low").lower()
        emoji = get_severity_emoji(severity)
        title = article.get("title", "")
        url = article.get("url", "")
        summary = article.get("summary", "").strip()
        category = article.get("category", "general").capitalize()
        source = article.get("source", "")

        if not summary:
            summary = "Brief: Unable to generate AI summary. Click 'Read more' for the full technical report."

        lines.append(
            f"\n<b>{i}. {emoji} [{severity.upper()}] {title}</b>\n"
            f"{summary}\n"
            f"<i>Category: {category} | Source: {source}</i>\n"
            f"<a href='{url}'>Read more</a>"
        )

    message = "\n".join(lines)
    return send_message(message)


def send_critical_alert(cve: dict) -> bool:
    """
    Send an instant alert for a critical CVE.

    Args:
        cve: CVE dict from database with id, description, score.

    Returns:
        True if sent successfully, False otherwise.
    """
    cve_id = cve.get("cve_id", "Unknown")
    description = cve.get("description", "")
    cvss_score = cve.get("cvss_score", 0.0)
    is_exploited = cve.get("is_exploited", 0)

    exploited_tag = "⚠️ ACTIVELY EXPLOITED" if is_exploited else ""

    message = (
        f"🚨 <b>CRITICAL CVE ALERT</b> 🚨\n\n"
        f"<b>ID:</b> {cve_id}\n"
        f"<b>CVSS Score:</b> {cvss_score}/10\n"
        f"{exploited_tag}\n\n"
        f"<b>Description:</b>\n{description}\n\n"
        f"<i>SentinelAI — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</i>"
    )

    return send_message(message)