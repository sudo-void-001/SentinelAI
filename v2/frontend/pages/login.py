"""
pages/login.py — Login and signup page for SentinelAI V2.

Premium dark UI with JWT authentication.
Design: void black, red accent, JetBrains Mono.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components.theme import apply_theme, logo
from components.api_client import login, signup

st.set_page_config(
    page_title="SentinelAI V2 — Login",
    page_icon="🛡",
    layout="centered",
)

apply_theme()


def render_login():
    """Render the login form."""
    st.markdown("""
    <div style="text-align:center;margin-bottom:32px;">
        <div style="font-family:'Syne',sans-serif;font-size:32px;
                    font-weight:800;letter-spacing:0.08em;
                    color:#e8edf3;margin-bottom:8px;">
            SENTINEL<span style="color:#e63946;">AI</span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;
                    font-size:11px;color:#3d5166;
                    letter-spacing:0.12em;">
            CYBER THREAT INTELLIGENCE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#0d1117;border:1px solid #1e2d3d;
                border-radius:12px;padding:32px;
                max-width:400px;margin:0 auto;">
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        username = st.text_input("Username", key="login_username", placeholder="your_username")
        password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        if st.button("Login", key="login_btn"):
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Authenticating..."):
                    result = login(username, password)
                if result:
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials or account disabled.")

    with tab2:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        new_username = st.text_input("Username", key="signup_username", placeholder="choose_username")
        new_email = st.text_input("Email", key="signup_email", placeholder="your@email.com")
        new_password = st.text_input("Password", type="password", key="signup_password", placeholder="••••••••")
        invite_code = st.text_input("Invite Code", key="signup_invite", placeholder="xxxx-xxxx")

        st.markdown("""
        <div style="font-size:11px;color:#3d5166;
                    font-family:'JetBrains Mono',monospace;
                    margin-top:8px;">
            SentinelAI is invite-only. Contact admin for access.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        if st.button("Create Account", key="signup_btn"):
            if not all([new_username, new_email, new_password, invite_code]):
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Creating account..."):
                    result = signup(new_username, new_email, new_password, invite_code)
                if result:
                    st.success("Account created! Welcome to SentinelAI.")
                    st.rerun()
                else:
                    st.error("Invalid invite code or username/email already taken.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:24px;">
        <span style="font-family:'JetBrains Mono',monospace;
                     font-size:10px;color:#1e2d3d;">
            PRIVATE PLATFORM — INVITE ONLY
        </span>
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN ─────────────────────────────────────────

if st.session_state.get("token"):
    st.switch_page("pages/dashboard.py")
else:
    render_login()