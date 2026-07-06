"""
components/theme.py — Global CSS theme for SentinelAI V2.
Injected into every page to override Streamlit defaults.
"""

import streamlit as st


THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Syne:wght@700;800&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stSidebarNav"] {display: none !important;}

:root {
    --bg-void:     #080b10;
    --bg-surface:  #0d1117;
    --bg-card:     #111820;
    --bg-elevated: #161f2a;
    --border:      #1e2d3d;
    --red:         #e63946;
    --red-glow:    rgba(230,57,70,0.15);
    --teal:        #2ec4b6;
    --amber:       #f4a261;
    --blue:        #4895ef;
    --text-primary:   #e8edf3;
    --text-secondary: #7a8fa6;
    --text-dim:       #3d5166;
}

.stApp {
    background-color: var(--bg-void) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

.main .block-container {
    background-color: var(--bg-void) !important;
    padding-top: 2rem !important;
    max-width: 1200px !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput input {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 10px 14px !important;
}

.stTextInput input:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 2px var(--red-glow) !important;
}

.stTextInput label {
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

.stButton button {
    background-color: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 20px rgba(230,57,70,0.3) !important;
    width: 100% !important;
}

.stButton button:hover {
    background-color: #ff4d5a !important;
    box-shadow: 0 0 28px rgba(230,57,70,0.5) !important;
    transform: translateY(-1px) !important;
}

.stSelectbox select,
[data-testid="stSelectbox"] > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

[data-testid="stMetric"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="stMetricValue"] {
    color: var(--red) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stDataFrame"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

hr {
    border-color: var(--border) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg-surface) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 8px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--red-glow) !important;
    color: var(--red) !important;
    border-bottom: 2px solid var(--red) !important;
}

.stAlert {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 2px;
}

.sentinel-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}

.sentinel-card-red { border-left: 4px solid var(--red); }
.sentinel-card-teal { border-left: 4px solid var(--teal); }
.sentinel-card-amber { border-left: 4px solid var(--amber); }
.sentinel-card-blue { border-left: 4px solid var(--blue); }

.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    font-family: 'JetBrains Mono', monospace;
}

.badge-critical {
    background: rgba(230,57,70,0.15);
    color: #e63946;
    border: 1px solid rgba(230,57,70,0.3);
}

.badge-high {
    background: rgba(244,162,97,0.12);
    color: #f4a261;
    border: 1px solid rgba(244,162,97,0.25);
}

.badge-medium {
    background: rgba(72,149,239,0.12);
    color: #4895ef;
    border: 1px solid rgba(72,149,239,0.25);
}

.badge-low {
    background: rgba(46,196,182,0.12);
    color: #2ec4b6;
    border: 1px solid rgba(46,196,182,0.25);
}

.mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--text-secondary);
}

.sentinel-logo {
    font-family: 'Syne', sans-serif;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--text-primary);
}

.sentinel-logo span { color: var(--red); }
</style>
"""


def apply_theme():
    """Inject SentinelAI theme CSS into current page."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def card(content: str, variant: str = "") -> None:
    """
    Render a styled card component.

    Args:
        content: HTML content inside the card.
        variant: Color variant — red, teal, amber, blue, or empty.
    """
    css_class = f"sentinel-card sentinel-card-{variant}" if variant else "sentinel-card"
    st.markdown(f'<div class="{css_class}">{content}</div>', unsafe_allow_html=True)


def badge(severity: str) -> str:
    """
    Return HTML badge string for a severity level.

    Args:
        severity: critical, high, medium, or low.

    Returns:
        HTML badge string.
    """
    return f'<span class="badge badge-{severity.lower()}">{severity.upper()}</span>'


def logo() -> None:
    """Render SentinelAI logo."""
    st.markdown(
        '<div class="sentinel-logo">SENTINEL<span>AI</span></div>',
        unsafe_allow_html=True
    )