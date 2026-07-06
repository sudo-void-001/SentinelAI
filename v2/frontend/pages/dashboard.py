"""
pages/dashboard.py — Main threat intelligence dashboard.

Shows live articles, CVEs, stats, and severity breakdown.
Design: void black, red accent, premium dark UI.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from components.theme import apply_theme, badge, card
from components.api_client import get_articles, get_cves, get_stats

st.set_page_config(
    page_title="SentinelAI — Dashboard",
    page_icon="🛡",
    layout="wide",
)

apply_theme()

# ─── AUTH GUARD ───────────────────────────────────
if not st.session_state.get("token"):
    st.switch_page("pages/login.py")

# ─── HEADER ───────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div style="margin-bottom:8px;">
        <div style="font-family:'Syne',sans-serif;font-size:22px;
                    font-weight:800;color:#e8edf3;">
            Threat Dashboard
        </div>
        <div style="font-family:'JetBrains Mono',monospace;
                    font-size:11px;color:#3d5166;">
            Real-time cybersecurity intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align:right;font-family:'JetBrains Mono',monospace;
                font-size:11px;color:#3d5166;">
        {datetime.utcnow().strftime("%b %d, %Y — %H:%M UTC")}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─── STATS ROW ────────────────────────────────────
stats = get_stats()

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Articles", stats.get("total_articles", 0))
with c2:
    st.metric("🔴 Critical", stats.get("critical", 0))
with c3:
    st.metric("🟠 High", stats.get("high", 0))
with c4:
    st.metric("🟡 Medium", stats.get("medium", 0))
with c5:
    st.metric("CVEs Tracked", stats.get("total_cves", 0))

st.markdown("<hr>", unsafe_allow_html=True)

# ─── FILTERS ──────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
with col_f1:
    severity_filter = st.selectbox(
        "Severity",
        ["All", "critical", "high", "medium", "low"],
        key="sev_filter"
    )
with col_f2:
    category_filter = st.selectbox(
        "Category",
        ["All", "ransomware", "vulnerability", "breach", "malware", "patch", "phishing"],
        key="cat_filter"
    )
with col_f3:
    limit = st.selectbox("Show", [10, 20, 50], key="limit_filter")

# ─── TABS ─────────────────────────────────────────
tab1, tab2 = st.tabs(["🔥 Threat Feed", "⚠️ CVE Tracker"])

with tab1:
    sev = None if severity_filter == "All" else severity_filter
    cat = None if category_filter == "All" else category_filter
    articles = get_articles(limit=limit, severity=sev, category=cat)

    if not articles:
        st.markdown("""
        <div style="text-align:center;padding:48px;color:#3d5166;
                    font-family:'JetBrains Mono',monospace;">
            No articles found. Run V1 pipeline to collect data.
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
                "low": "teal"
            }
            variant = variant_map.get(severity, "")

            card(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                {badge(severity)}
                <span style="background:#1e2d3d;color:#7a8fa6;
                             padding:2px 7px;border-radius:4px;
                             font-size:10px;font-family:'JetBrains Mono',monospace;">
                    {category}
                </span>
                <span style="color:#3d5166;font-size:10px;
                             font-family:'JetBrains Mono',monospace;
                             margin-left:auto;">
                    {source}
                </span>
            </div>
            <div style="font-size:14px;font-weight:600;
                        color:#e8edf3;margin-bottom:6px;">
                {title}
            </div>
            <div style="font-size:12px;color:#7a8fa6;
                        line-height:1.6;margin-bottom:10px;">
                {summary}
            </div>
            <a href="{url}" target="_blank"
               style="color:#e63946;font-size:12px;
                      font-weight:600;text-decoration:none;">
                Read more →
            </a>
            """, variant=variant)

with tab2:
    cves = get_cves(limit=limit)

    if not cves:
        st.markdown("""
        <div style="text-align:center;padding:48px;color:#3d5166;
                    font-family:'JetBrains Mono',monospace;">
            No CVEs found. Run V1 pipeline to collect data.
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
                <span style="background:rgba(230,57,70,0.15);
                             color:#e63946;padding:2px 8px;
                             border-radius:4px;font-size:10px;
                             font-weight:700;font-family:'JetBrains Mono',monospace;">
                    ⚡ ACTIVELY EXPLOITED
                </span>
                """

            card(f"""
            <div style="display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:8px;">
                <span style="font-family:'JetBrains Mono',monospace;
                             font-size:13px;font-weight:700;
                             color:#e63946;">
                    {cve_id}
                </span>
                <div style="display:flex;gap:8px;align-items:center;">
                    {exploited_html}
                    {badge(severity)}
                    <span style="font-family:'JetBrains Mono',monospace;
                                 font-size:12px;font-weight:700;
                                 color:#f4a261;">
                        CVSS {cvss_score}
                    </span>
                </div>
            </div>
            <div style="font-size:12px;color:#7a8fa6;line-height:1.5;">
                {description[:200]}...
            </div>
            """, variant="red" if severity == "critical" else "amber")