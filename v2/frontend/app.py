"""
app.py — SentinelAI V2 Streamlit entry point.

Handles routing between pages based on auth state.
Run with: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from components.theme import apply_theme
from components.api_client import logout

st.set_page_config(
    page_title="SentinelAI V2",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()


def render_sidebar():
    """Render navigation sidebar for authenticated users."""
    with st.sidebar:
        st.markdown("""
        <div style="padding:16px 0;border-bottom:1px solid #1e2d3d;
                    margin-bottom:16px;">
            <div style="font-family:'Syne',sans-serif;font-size:18px;
                        font-weight:800;letter-spacing:0.08em;
                        color:#e8edf3;">
                SENTINEL<span style="color:#e63946;">AI</span>
            </div>
            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:10px;color:#3d5166;
                        letter-spacing:0.1em;margin-top:4px;">
                V2.0.0 — ONLINE
            </div>
        </div>
        """, unsafe_allow_html=True)

        username = st.session_state.get("username", "")
        role = st.session_state.get("role", "user")

        st.markdown(f"""
        <div style="padding:10px 12px;background:#111820;
                    border:1px solid #1e2d3d;border-radius:8px;
                    margin-bottom:16px;">
            <div style="font-size:12px;color:#7a8fa6;
                        font-family:'JetBrains Mono',monospace;">
                Logged in as
            </div>
            <div style="font-size:14px;color:#e8edf3;
                        font-weight:600;margin-top:2px;">
                {username}
            </div>
            <div style="font-size:10px;color:#e63946;
                        font-family:'JetBrains Mono',monospace;
                        letter-spacing:0.06em;margin-top:2px;">
                {role.upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link("pages/dashboard.py", label="Dashboard", icon="🛡")
        st.page_link("pages/settings.py", label="Settings", icon="⚙️")

        if role == "admin":
            st.markdown("""
            <div style="font-size:10px;color:#3d5166;
                        font-family:'JetBrains Mono',monospace;
                        letter-spacing:0.1em;text-transform:uppercase;
                        padding:12px 0 6px 0;">
                Admin
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/admin.py", label="Admin Panel", icon="🔧")

        st.markdown('<div style="flex:1;"></div>', unsafe_allow_html=True)

        if st.button("Logout", key="logout_btn"):
            logout()
            st.rerun()


# ─── ROUTING ──────────────────────────────────────

if not st.session_state.get("token"):
    st.switch_page("pages/login.py")
else:
    render_sidebar()
    st.switch_page("pages/dashboard.py")