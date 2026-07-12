"""
core/scheduler_v2.py — V2 email digest scheduler.
All imports inside functions to prevent circular imports.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def send_digest_for_slot(hour: int) -> None:
    """
    Send digest email to all users assigned to this hour slot.

    Args:
        hour: IST hour (6-12) to send digest for.
    """
    # All imports inside function — prevents circular import
    from core.database import SessionLocal
    from models.user import User
    import smtplib
    import os
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from datetime import datetime

    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    DASHBOARD_URL = os.getenv("DASHBOARD_URL", "https://your-frontend.onrender.com")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print(f"[scheduler_v2] Email not configured. Skipping slot {hour}.")
        return

    db = SessionLocal()
    try:
        users = db.query(User).filter(
            User.digest_slot == hour,
            User.is_active == True,
            User.notify_email == True,
        ).all()

        if not users:
            print(f"[scheduler_v2] No users for slot {hour}:00 IST")
            return

        # Fetch live articles from RSS
        articles = _fetch_articles()
        cves = _fetch_cves()

        for user in users:
            if not user.email:
                continue
            try:
                _send_email(
                    to_email=user.email,
                    username=user.username,
                    articles=articles,
                    cves=cves,
                    email_address=EMAIL_ADDRESS,
                    email_password=EMAIL_PASSWORD,
                    dashboard_url=DASHBOARD_URL,
                )
                print(f"[scheduler_v2] ✅ Digest sent to {user.email}")
            except Exception as e:
                print(f"[scheduler_v2] ❌ Failed {user.email}: {e}")
    finally:
        db.close()


def _fetch_articles(limit: int = 10) -> list:
    """Fetch live articles from RSS feeds."""
    import feedparser
    from datetime import datetime

    feeds = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/",
        "https://krebsonsecurity.com/feed/",
    ]

    articles = []
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                title = entry.get("title", "")
                url = entry.get("link", "")
                if not title or not url:
                    continue
                articles.append({
                    "title": title,
                    "url": url,
                    "source": feed.feed.get("title", "Security News"),
                    "summary": entry.get("summary", "")[:200] if entry.get("summary") else "",
                    "severity": "high",
                    "category": "general",
                })
        except Exception as e:
            print(f"[scheduler_v2] RSS failed {feed_url}: {e}")

    return articles[:limit]


def _fetch_cves(limit: int = 5) -> list:
    """Fetch recent CVEs from CISA KEV."""
    import requests
    from datetime import datetime

    cves = []
    try:
        response = requests.get(
            "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        for vuln in data.get("vulnerabilities", [])[:limit]:
            cvss = 8.0
            severity = "high"
            cves.append({
                "cve_id": vuln.get("cveID", ""),
                "description": vuln.get("shortDescription", ""),
                "cvss_score": cvss,
                "severity": severity,
                "is_exploited": 1,
                "affected_products": vuln.get("product", ""),
            })
    except Exception as e:
        print(f"[scheduler_v2] CISA KEV failed: {e}")

    return cves


def _send_email(
    to_email: str,
    username: str,
    articles: list,
    cves: list,
    email_address: str,
    email_password: str,
    dashboard_url: str,
) -> None:
    """Build and send HTML digest email via Gmail SMTP."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from datetime import datetime

    date_str = datetime.utcnow().strftime("%B %d, %Y")

    severity_colors = {
        "critical": "#c0392b",
        "high": "#d4851a",
        "medium": "#2471a3",
        "low": "#27ae60",
    }

    articles_html = ""
    for article in articles[:5]:
        severity = article.get("severity", "high").lower()
        color = severity_colors.get(severity, "#d4851a")
        title = article.get("title", "")
        summary = article.get("summary", "") or "Click Read more for full article."
        source = article.get("source", "")
        url = article.get("url", "#")

        articles_html += f"""
        <div style="background:#ede8dc;border:1px solid #d4c4a0;
                    border-left:4px solid {color};border-radius:6px;
                    padding:14px;margin-bottom:10px;">
            <div style="margin-bottom:6px;">
                <span style="background:{color}22;color:{color};
                             padding:2px 8px;border-radius:3px;
                             font-size:10px;font-weight:700;
                             font-family:monospace;">
                    {severity.upper()}
                </span>
                <span style="color:#8b6f47;font-size:10px;
                             font-family:monospace;margin-left:8px;">
                    {source}
                </span>
            </div>
            <div style="font-size:14px;font-weight:600;
                        color:#2c1810;margin-bottom:6px;">
                {title}
            </div>
            <div style="font-size:12px;color:#5c3d2e;
                        margin-bottom:8px;line-height:1.5;">
                {summary[:150]}...
            </div>
            <a href="{url}" style="color:#a8873a;font-size:12px;
                                   font-weight:600;text-decoration:none;">
                Read more →
            </a>
        </div>
        """

    cves_html = ""
    for cve in cves[:3]:
        cve_id = cve.get("cve_id", "")
        description = cve.get("description", "")[:120]
        score = cve.get("cvss_score", 0)

        cves_html += f"""
        <div style="background:#ede8dc;border:1px solid #d4c4a0;
                    border-left:4px solid #c0392b;border-radius:6px;
                    padding:12px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;
                        margin-bottom:4px;">
                <span style="font-family:monospace;font-size:13px;
                             font-weight:700;color:#c0392b;">
                    {cve_id}
                </span>
                <span style="font-family:monospace;font-size:11px;
                             color:#d4851a;font-weight:700;">
                    ⚡ EXPLOITED · CVSS {score}
                </span>
            </div>
            <div style="font-size:12px;color:#5c3d2e;">
                {description}...
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f5f0e8;
                 font-family:-apple-system,Inter,sans-serif;">
        <div style="max-width:580px;margin:0 auto;padding:24px 16px;">

            <div style="background:#1a1008;border-radius:10px;
                        padding:24px;text-align:center;
                        margin-bottom:16px;">
                <div style="font-size:28px;font-weight:700;
                            color:#c9a84c;letter-spacing:0.04em;
                            margin-bottom:6px;">
                    SentinelAI
                </div>
                <div style="width:40px;height:1px;
                            background:#c9a84c;
                            margin:0 auto 10px auto;opacity:0.4;">
                </div>
                <div style="font-size:10px;color:#5c3d2e;
                            letter-spacing:0.16em;
                            font-family:monospace;">
                    DAILY THREAT DIGEST · {date_str}
                </div>
                <div style="font-size:13px;color:#8b6f47;
                            margin-top:8px;">
                    Good morning, {username}
                </div>
            </div>

            <div style="text-align:center;margin-bottom:16px;">
                <a href="{dashboard_url}"
                   style="display:inline-block;
                          background:linear-gradient(135deg,#c9a84c,#a8873a);
                          color:#1a1008;padding:12px 32px;
                          border-radius:6px;text-decoration:none;
                          font-weight:700;font-size:13px;
                          letter-spacing:0.06em;">
                    View Full Dashboard →
                </a>
            </div>

            <div style="background:#f5f0e8;border:1px solid #d4c4a0;
                        border-radius:8px;padding:16px;
                        margin-bottom:12px;">
                <div style="font-size:10px;font-weight:700;
                            color:#8b6f47;letter-spacing:0.12em;
                            text-transform:uppercase;margin-bottom:12px;">
                    Today's Threat Feed
                </div>
                {articles_html if articles_html else
                 '<p style="color:#8b6f47;font-size:13px;">No articles collected yet.</p>'}
            </div>

            <div style="background:#f5f0e8;border:1px solid #d4c4a0;
                        border-radius:8px;padding:16px;
                        margin-bottom:12px;">
                <div style="font-size:10px;font-weight:700;
                            color:#8b6f47;letter-spacing:0.12em;
                            text-transform:uppercase;margin-bottom:12px;">
                    Actively Exploited CVEs
                </div>
                {cves_html if cves_html else
                 '<p style="color:#8b6f47;font-size:13px;">No CVEs collected yet.</p>'}
            </div>

            <div style="text-align:center;padding:16px 0;">
                <div style="font-size:10px;color:#b8a882;
                            font-family:monospace;letter-spacing:0.08em;">
                    SENTINELAI V2 · PRIVATE PLATFORM · INVITE ONLY
                </div>
                <div style="font-size:10px;color:#b8a882;
                            margin-top:4px;">
                    Built by Rajesh Pattan
                </div>
            </div>

        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🛡 SentinelAI Daily Digest — {date_str}"
    msg["From"] = f"SentinelAI <{email_address}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))
    import os
    import resend

    resend.api_key = os.getenv("RESEND_API_KEY")

    resend.Emails.send({
    "from": "SentinelAI <onboarding@resend.dev>",
    "to": [to_email],
    "subject": f"🛡 SentinelAI Daily Digest — {date_str}",
    "html": html,
})


def start_v2_scheduler() -> BackgroundScheduler:
    """Start background scheduler for all IST digest slots."""
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    for hour in [6, 7, 8, 9, 10, 11, 12]:
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