"""
pages/login.py — Login and signup page for SentinelAI V2.
Luxury Bloomberg Terminal aesthetic.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components.theme import apply_theme
from components.api_client import login, signup

st.set_page_config(
    page_title="SentinelAI — Sign In",
    page_icon="🛡",
    layout="centered",
)

apply_theme()

if st.session_state.get("token"):
    st.switch_page("pages/dashboard.py")

# ─── HERO ─────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:48px 0 32px 0;">
    <div style="font-family:'Playfair Display',serif;
                font-size:42px;font-weight:700;
                color:#2c1810;letter-spacing:0.02em;
                margin-bottom:8px;">
        SentinelAI
    </div>
    <div style="width:60px;height:2px;
                background:linear-gradient(90deg,transparent,#c9a84c,transparent);
                margin:0 auto 16px auto;">
    </div>
    <div style="font-family:'JetBrains Mono',monospace;
                font-size:11px;color:#8b6f47;
                letter-spacing:0.16em;text-transform:uppercase;">
        Cyber Threat Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CARD ─────────────────────────────────────────
st.markdown("""
<div style="background:#ede8dc;border:1px solid #d4c4a0;
            border-radius:10px;padding:32px;
            max-width:420px;margin:0 auto;
            box-shadow:0 4px 24px rgba(44,24,16,0.08);">
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Sign In", "Create Account"])

with tab1:
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    username = st.text_input(
        "Username",
        key="login_username",
        placeholder="your_username"
    )
    password = st.text_input(
        "Password",
        type="password",
        key="login_password",
        placeholder="••••••••"
    )
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    if st.button("Sign In →", key="login_btn"):
        if not username or not password:
            st.error("Please enter your credentials.")
        else:
            with st.spinner("Authenticating..."):
                result = login(username, password)
            if result:
                st.rerun()
            else:
                st.error("Invalid credentials or account disabled.")

with tab2:
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    new_username = st.text_input(
        "Username",
        key="signup_username",
        placeholder="choose_username"
    )
    new_email = st.text_input(
        "Email Address",
        key="signup_email",
        placeholder="your@email.com"
    )
    new_password = st.text_input(
        "Password",
        type="password",
        key="signup_password",
        placeholder="min. 8 characters"
    )
    invite_code = st.text_input(
        "Invite Code",
        key="signup_invite",
        placeholder="provided by admin"
    )

    st.markdown("""
    <div style="font-size:11px;color:#8b6f47;
                font-family:'JetBrains Mono',monospace;
                margin-top:6px;padding:8px 10px;
                background:rgba(201,168,76,0.08);
                border-radius:4px;border-left:2px solid #c9a84c;">
        Access is by invitation only.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    if st.button("Create Account →", key="signup_btn"):
        if not all([new_username, new_email, new_password, invite_code]):
            st.error("All fields are required.")
        else:
            with st.spinner("Creating account..."):
                result = signup(
                    new_username, new_email,
                    new_password, invite_code
                )
            if result:
                st.rerun()
            else:
                st.error("Invalid invite code or credentials already in use.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:24px;">
    <span style="font-family:'JetBrains Mono',monospace;
                 font-size:10px;color:#b8a882;
                 letter-spacing:0.08em;">
        PRIVATE PLATFORM · INVITE ONLY
    </span>
</div>
""", unsafe_allow_html=True)