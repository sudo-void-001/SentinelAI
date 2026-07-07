"""
pages/dashboard.py — Main threat intelligence dashboard.
Luxury Bloomberg Terminal aesthetic.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from components.theme import apply_theme, badge, card, page_header, sidebar_nav
from components.api_client import get_articles, get_cves, get_stats

st.set_page_config(
    page_title="SentinelAI — Dashboard",
    page_icon="🛡",
    layout="wide",
)

apply_theme()

if not st.session_state.get("token"):
    st.switch_page("pages/login.py")

username = st.session_state.get("username", "")
role = st.session_state.get("role", "user")

sidebar_nav(username, role)

# ─── HEADER ───────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    page_header(
        "Threat Dashboard",
        f"Live intelligence · {datetime.utcnow().strftime('%B %d, %Y')}"
    )
with col2:
    st.markdown(f"""
    <div style="text-align:right;padding-top:8px;">
        <div style="font-family:'JetBrains Mono',monospace;
                    font-size:11px;color:#8b6f47;">
            {datetime.utcnow().strftime("%H:%M UTC")}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── STATS ────────────────────────────────────────
stats = get_stats()

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Articles", stats.get("total_articles", 0))
with c2:
    st.metric("Critical", stats.get("critical", 0))
with c3:
    st.metric("High", stats.get("high", 0))
with c4:
    st.metric("Medium", stats.get("medium", 0))
with c5:
    st.metric("CVEs Tracked", stats.get("total_cves", 0))

st.markdown("<hr>", unsafe_allow_html=True)

# ─── FILTERS ──────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
with col_f1:
    severity_filter = st.selectbox(
        "Severity",
        ["All", "critical", "high", "medium", "low"],
        key="sev_filter"
    )
with col_f2:
    category_filter = st.selectbox(
        "Category",
        ["All", "ransomware", "vulnerability", "breach",
         "malware", "patch", "phishing"],
        key="cat_filter"
    )
with col_f3:
    limit = st.selectbox("Show", [10, 20, 50], key="limit_filter")

# ─── TABS ─────────────────────────────────────────
tab1, tab2 = st.tabs(["Threat Feed", "CVE Tracker"])

with tab1:
    sev = None if severity_filter == "All" else severity_filter
    cat = None if category_filter == "All" else category_filter
    articles = get_articles(limit=limit, severity=sev, category=cat)

    if not articles:
        st.markdown("""
        <div style="text-align:center;padding:48px;
                    color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    font-size:12px;">
            No articles found. Run the V1 pipeline to collect data.
        </div>
        """, unsafe_allow_html=True)
    else:
        for article in articles:
            severity = article.get("severity", "low")
            title = article.get("title", "")
            summary = article.get("summary", "No summary available.")
            source = article.get("source", "")
            url = article.get("url", "#")
            category = article.get("category", "general")

            variant_map = {
                "critical": "red",
                "high": "amber",
                "medium": "blue",
                "low": "green"
            }
            variant = variant_map.get(severity, "gold")

            card(f"""
            <div style="display:flex;align-items:center;
                        gap:8px;margin-bottom:10px;">
                {badge(severity)}
                <span style="background:rgba(44,24,16,0.08);
                             color:#8b6f47;padding:2px 7px;
                             border-radius:3px;font-size:10px;
                             font-family:'JetBrains Mono',monospace;
                             text-transform:uppercase;
                             letter-spacing:0.04em;">
                    {category}
                </span>
                <span style="color:#b8a882;font-size:10px;
                             font-family:'JetBrains Mono',monospace;
                             margin-left:auto;">
                    {source}
                </span>
            </div>
            <div style="font-size:15px;font-weight:600;
                        color:#2c1810;margin-bottom:6px;
                        font-family:'Inter',sans-serif;
                        line-height:1.4;">
                {title}
            </div>
            <div style="font-size:13px;color:#5c3d2e;
                        line-height:1.7;margin-bottom:10px;">
                {summary}
            </div>
            <a href="{url}" target="_blank"
               style="color:#a8873a;font-size:12px;
                      font-weight:600;text-decoration:none;
                      font-family:'JetBrains Mono',monospace;
                      letter-spacing:0.02em;">
                Read full article →
            </a>
            """, variant=variant)

with tab2:
    cves = get_cves(limit=limit)

    if not cves:
        st.markdown("""
        <div style="text-align:center;padding:48px;
                    color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    font-size:12px;">
            No CVEs found. Run the V1 pipeline to collect data.
        </div>
        """, unsafe_allow_html=True)
    else:
        for cve in cves:
            cve_id = cve.get("cve_id", "")
            description = cve.get("description", "")
            cvss_score = cve.get("cvss_score", 0.0)
            severity = cve.get("severity", "low")
            is_exploited = cve.get("is_exploited", 0)

            exploited_html = ""
            if is_exploited:
                exploited_html = """
                <span style="background:rgba(192,57,43,0.1);
                             color:#c0392b;padding:2px 8px;
                             border-radius:3px;font-size:10px;
                             font-weight:700;
                             font-family:'JetBrains Mono',monospace;">
                    ⚡ ACTIVELY EXPLOITED
                </span>
                """

            card(f"""
            <div style="display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:8px;">
                <span style="font-family:'JetBrains Mono',monospace;
                             font-size:14px;font-weight:700;
                             color:#a8873a;letter-spacing:0.02em;">
                    {cve_id}
                </span>
                <div style="display:flex;gap:8px;align-items:center;">
                    {exploited_html}
                    {badge(severity)}
                    <span style="font-family:'JetBrains Mono',monospace;
                                 font-size:12px;font-weight:700;
                                 color:#5c3d2e;">
                        CVSS {cvss_score}
                    </span>
                </div>
            </div>
            <div style="font-size:13px;color:#5c3d2e;
                        line-height:1.6;">
                {description[:200]}...
            </div>
            """, variant="red" if severity == "critical" else "amber")