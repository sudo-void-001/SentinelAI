"""
components/theme.py — SentinelAI V2 Luxury Theme.
Bloomberg Terminal meets luxury brand.
Dark espresso sidebar, warm cream content, gold accents.
"""

import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stSidebarNav"] {display: none !important;}

:root {
    --sidebar-bg:    #1a1008;
    --sidebar-text:  #c9a84c;
    --content-bg:    #f5f0e8;
    --card-bg:       #ede8dc;
    --card-hover:    #e5dece;
    --border:        #d4c4a0;
    --border-dark:   #b8a882;
    --gold:          #c9a84c;
    --gold-dark:     #a8873a;
    --gold-light:    #e8d5a3;
    --gold-glow:     rgba(201,168,76,0.15);
    --brown-deep:    #2c1810;
    --brown-mid:     #5c3d2e;
    --brown-muted:   #8b6f47;
    --brown-light:   #b8956a;
    --cream:         #f5f0e8;
    --parchment:     #ede8dc;
    --text-primary:  #2c1810;
    --text-secondary:#5c3d2e;
    --text-dim:      #8b6f47;
    --red-alert:     #c0392b;
    --green-safe:    #27ae60;
    --amber-warn:    #d4851a;
    --blue-info:     #2471a3;
}

/* ─── GLOBAL ─── */
.stApp {
    background-color: var(--content-bg) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

.main .block-container {
    background-color: var(--content-bg) !important;
    padding-top: 2rem !important;
    max-width: 1200px !important;
}

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid #3d2510 !important;
}

[data-testid="stSidebar"] * {
    color: #c9a84c !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] .stButton button {
    background-color: transparent !important;
    color: #8b6f47 !important;
    border: 1px solid #3d2510 !important;
    box-shadow: none !important;
    width: 100% !important;
    text-align: left !important;
    font-size: 13px !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    transition: all 0.2s !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    background-color: #2c1810 !important;
    color: #c9a84c !important;
    border-color: #c9a84c !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ─── INPUTS ─── */
.stTextInput input {
    background-color: var(--parchment) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 10px 14px !important;
    font-size: 13px !important;
}

.stTextInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px var(--gold-glow) !important;
}

.stTextInput label {
    color: var(--text-dim) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ─── BUTTONS ─── */
.stButton button {
    background: linear-gradient(135deg, #c9a84c 0%, #a8873a 100%) !important;
    color: #1a1008 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 24px !important;
    letter-spacing: 0.04em !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(201,168,76,0.3), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #d4b85c 0%, #c9a84c 100%) !important;
    box-shadow: 0 4px 16px rgba(201,168,76,0.45), inset 0 1px 0 rgba(255,255,255,0.25) !important;
    transform: translateY(-2px) !important;
}

.stButton button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 1px 4px rgba(201,168,76,0.3) !important;
}

/* ─── SELECTBOX ─── */
[data-testid="stSelectbox"] > div > div {
    background-color: var(--parchment) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text-primary) !important;
}

/* ─── METRICS ─── */
[data-testid="stMetric"] {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 16px !important;
}

[data-testid="stMetricValue"] {
    color: var(--gold-dark) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-dim) !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background-color: var(--parchment) !important;
    border-bottom: 2px solid var(--border) !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: var(--text-dim) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 8px 16px !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--card-bg) !important;
    color: var(--gold-dark) !important;
    border-bottom: 2px solid var(--gold) !important;
}

/* ─── DATAFRAME ─── */
[data-testid="stDataFrame"] {
    background-color: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ─── ALERTS ─── */
.stAlert {
    background-color: var(--parchment) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ─── HR ─── */
hr {
    border-color: var(--border) !important;
    opacity: 0.6 !important;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--parchment); }
::-webkit-scrollbar-thumb {
    background: var(--border-dark);
    border-radius: 3px;
}

/* ─── PAGE LINKS ─── */
[data-testid="stPageLink"] {
    border-radius: 6px !important;
    margin-bottom: 4px !important;
    transition: all 0.2s !important;
}

[data-testid="stPageLink"]:hover {
    background-color: #2c1810 !important;
}

[data-testid="stPageLink"] p {
    color: #8b6f47 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ─── CUSTOM COMPONENTS ─── */
.sentinel-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.2s;
}

.sentinel-card:hover {
    background: var(--card-hover);
    border-color: var(--border-dark);
}

.sentinel-card-gold { border-left: 3px solid var(--gold); }
.sentinel-card-red { border-left: 3px solid var(--red-alert); }
.sentinel-card-green { border-left: 3px solid var(--green-safe); }
.sentinel-card-amber { border-left: 3px solid var(--amber-warn); }
.sentinel-card-blue { border-left: 3px solid var(--blue-info); }

.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
}

.badge-critical {
    background: rgba(192,57,43,0.12);
    color: #c0392b;
    border: 1px solid rgba(192,57,43,0.25);
}

.badge-high {
    background: rgba(212,133,26,0.12);
    color: #d4851a;
    border: 1px solid rgba(212,133,26,0.25);
}

.badge-medium {
    background: rgba(36,113,163,0.1);
    color: #2471a3;
    border: 1px solid rgba(36,113,163,0.2);
}

.badge-low {
    background: rgba(39,174,96,0.1);
    color: #27ae60;
    border: 1px solid rgba(39,174,96,0.2);
}

.mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--text-dim);
}

.sentinel-logo {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: var(--gold);
}

.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--brown-deep);
    margin-bottom: 4px;
}

.page-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, var(--gold) 0%, transparent 100%);
    margin: 16px 0;
    opacity: 0.4;
}

.section-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-dim);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
</style>
"""


def apply_theme():
    """Inject SentinelAI luxury theme CSS."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def card(content: str, variant: str = "") -> None:
    """Render a styled luxury card."""
    css_class = f"sentinel-card sentinel-card-{variant}" if variant else "sentinel-card"
    st.markdown(f'<div class="{css_class}">{content}</div>', unsafe_allow_html=True)


def badge(severity: str) -> str:
    """Return HTML badge for severity level."""
    return f'<span class="badge badge-{severity.lower()}">{severity.upper()}</span>'


def page_header(title: str, subtitle: str = "") -> None:
    """Render a luxury page header."""
    st.markdown(f"""
    <div class="page-title">{title}</div>
    {f'<div class="page-subtitle">{subtitle}</div>' if subtitle else ''}
    <div class="divider"></div>
    """, unsafe_allow_html=True)


def sidebar_nav(username: str, role: str) -> None:
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:20px 0 16px 0;
                    border-bottom:1px solid #3d2510;
                    margin-bottom:16px;">
            <div style="font-family:'Playfair Display',serif;
                        font-size:20px;font-weight:700;
                        color:#c9a84c;letter-spacing:0.04em;">
                SentinelAI
            </div>
            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:9px;color:#5c3d2e;
                        letter-spacing:0.14em;margin-top:4px;
                        text-transform:uppercase;">
                Intelligence Platform
            </div>
        </div>

        <div style="padding:10px 12px;
                    background:rgba(201,168,76,0.08);
                    border:1px solid #3d2510;
                    border-radius:6px;margin-bottom:20px;">
            <div style="font-size:10px;color:#5c3d2e;
                        font-family:'JetBrains Mono',monospace;
                        letter-spacing:0.06em;text-transform:uppercase;">
                Signed in as
            </div>
            <div style="font-size:14px;color:#e8d5a3;
                        font-weight:600;margin-top:3px;">
                {username}
            </div>
            <div style="font-size:10px;color:#c9a84c;
                        font-family:'JetBrains Mono',monospace;
                        letter-spacing:0.08em;margin-top:2px;">
                {role.upper()}
            </div>
        </div>

        <div style="font-size:9px;color:#3d2510;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.12em;text-transform:uppercase;
                    margin-bottom:8px;padding-left:4px;">
            Navigation
        </div>
        """, unsafe_allow_html=True)

        st.page_link("pages/dashboard.py", label="Dashboard", icon="🛡")
        st.page_link("pages/settings.py", label="Settings", icon="⚙️")

        if role == "admin":
            st.markdown("""
            <div style="font-size:9px;color:#3d2510;
                        font-family:'JetBrains Mono',monospace;
                        letter-spacing:0.12em;text-transform:uppercase;
                        margin:16px 0 8px 0;padding-left:4px;">
                Administration
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/admin.py", label="Admin Panel", icon="🔧")

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

        if st.button("Sign Out", key="logout_btn"):
            from components.api_client import logout
            logout()
            st.rerun()

        st.markdown("""
        <div style="position:absolute;bottom:16px;left:0;right:0;
                    text-align:center;padding:0 16px;">
            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:9px;color:#3d2510;
                        letter-spacing:0.08em;">
                V2.0.0 · ONLINE
            </div>
        </div>
        """, unsafe_allow_html=True)