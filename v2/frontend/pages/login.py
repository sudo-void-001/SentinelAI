"""
pages/login.py — SentinelAI V2 Login Page.

Terminal boot sequence intro → login form.
Dark immersive pre-login. Cream shock post-login.
"""

import streamlit as st
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent))

from components.api_client import login, signup

st.set_page_config(
    page_title="SentinelAI — Access",
    page_icon="🛡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.stDeployButton {display:none;}
[data-testid="stSidebarNav"] {display:none !important;}
[data-testid="stSidebar"] {display:none !important;}
[data-testid="collapsedControl"] {display:none !important;}

.stApp {
    background-color: #080604 !important;
    font-family: 'Inter', sans-serif !important;
}

.main .block-container {
    background-color: transparent !important;
    padding-top: 0 !important;
    max-width: 500px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Terminal boot area */
.boot-terminal {
    background: #080604;
    border: 1px solid #2c1810;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
    font-family: 'JetBrains Mono', monospace;
    min-height: 200px;
}

.boot-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 2;
    margin: 0;
}

.boot-line-dim { color: #3d2510; }
.boot-line-gold { color: #c9a84c; }
.boot-line-green { color: #27ae60; }
.boot-line-red { color: #c0392b; }
.boot-line-white { color: #e8d5a3; }

/* Login form */
.login-form-wrap {
    background: #0d0a06;
    border: 1px solid #2c1810;
    border-radius: 10px;
    padding: 32px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.7);
}

/* Inputs */
.stTextInput input {
    background-color: #1a1008 !important;
    border: 1px solid #3d2510 !important;
    border-radius: 6px !important;
    color: #e8d5a3 !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 10px 14px !important;
    font-size: 13px !important;
    transition: border-color 0.2s !important;
}

.stTextInput input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.12) !important;
}

.stTextInput input::placeholder {
    color: #3d2510 !important;
}

.stTextInput label {
    color: #5c3d2e !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Primary button */
.stButton button {
    background: linear-gradient(135deg, #c9a84c 0%, #a8873a 100%) !important;
    color: #080604 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 2px 12px rgba(201,168,76,0.25),
                inset 0 1px 0 rgba(255,255,255,0.15) !important;
    cursor: pointer !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #d4b85c 0%, #c9a84c 100%) !important;
    box-shadow: 0 6px 24px rgba(201,168,76,0.4),
                inset 0 1px 0 rgba(255,255,255,0.2) !important;
    transform: translateY(-2px) !important;
}

.stButton button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(201,168,76,0.2) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    border-bottom: 1px solid #2c1810 !important;
    gap: 0 !important;
    margin-bottom: 20px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #3d2510 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stTabs [aria-selected="true"] {
    color: #c9a84c !important;
    border-bottom: 2px solid #c9a84c !important;
    background-color: transparent !important;
}

/* Alert */
.stAlert {
    background-color: #1a1008 !important;
    border: 1px solid #3d2510 !important;
    border-radius: 6px !important;
    color: #e8d5a3 !important;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2c1810; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

if st.session_state.get("token"):
    st.switch_page("pages/dashboard.py")

# ─── BOOT SEQUENCE ────────────────────────────────
if "boot_done" not in st.session_state:
    st.session_state.boot_done = False

if not st.session_state.boot_done:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 24px 0;">
        <div style="font-family:'Playfair Display',serif;
                    font-size:32px;font-weight:700;
                    color:#c9a84c;letter-spacing:0.04em;">
            SentinelAI
        </div>
        <div style="width:40px;height:1px;
                    background:linear-gradient(90deg,transparent,#c9a84c,transparent);
                    margin:10px auto;">
        </div>
    </div>
    """, unsafe_allow_html=True)

    boot_placeholder = st.empty()

    boot_lines = [
        ("dim",   "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"),
        ("gold",  "  SENTINELAI INTELLIGENCE PLATFORM v2.0.0"),
        ("dim",   "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"),
        ("dim",   ""),
        ("white", "  [ SYSTEM ] Initializing core modules..."),
        ("green", "  [ OK ]     Database engine loaded"),
        ("green", "  [ OK ]     Threat intelligence feeds online"),
        ("green", "  [ OK ]     CVE tracking active"),
        ("green", "  [ OK ]     AI summarization engine ready"),
        ("green", "  [ OK ]     Telegram gateway connected"),
        ("dim",   ""),
        ("white", "  [ SYSTEM ] Running security checks..."),
        ("green", "  [ OK ]     JWT authentication enabled"),
        ("green", "  [ OK ]     Invite-only access enforced"),
        ("green", "  [ OK ]     Session encryption active"),
        ("dim",   ""),
        ("gold",  "  [ READY ]  SentinelAI is online."),
        ("dim",   "  Awaiting authorized access..."),
        ("dim",   ""),
    ]

    displayed = []
    for style, line in boot_lines:
        displayed.append((style, line))
        html = '<div class="boot-terminal">'
        for s, l in displayed:
            color_class = f"boot-line-{s}"
            html += f'<p class="boot-line {color_class}">{l if l else "&nbsp;"}</p>'
        html += '</div>'
        boot_placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(0.08)

    time.sleep(0.4)
    st.session_state.boot_done = True
    st.rerun()

# ─── LOGO ─────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 24px 0;">
    <div style="font-family:'Playfair Display',serif;
                font-size:32px;font-weight:700;
                color:#c9a84c;letter-spacing:0.04em;
                margin-bottom:8px;">
        SentinelAI
    </div>
    <div style="width:40px;height:1px;
                background:linear-gradient(90deg,transparent,#c9a84c,transparent);
                margin:0 auto 10px auto;">
    </div>
    <div style="font-family:'JetBrains Mono',monospace;
                font-size:10px;color:#3d2510;
                letter-spacing:0.18em;text-transform:uppercase;">
        Cyber Threat Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

# ─── FORM ─────────────────────────────────────────
st.markdown('<div class="login-form-wrap">', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Sign In", "Create Account"])

with tab1:
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

    if st.button("Authenticate →", key="login_btn"):
        if not username or not password:
            st.error("Credentials required.")
        else:
            with st.spinner("Verifying..."):
                result = login(username, password)
            if result:
                st.session_state.boot_done = False
                st.rerun()
            else:
                st.error("Access denied. Invalid credentials.")

with tab2:
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
        placeholder="minimum 8 characters"
    )
    invite_code = st.text_input(
        "Invite Code",
        key="signup_invite",
        placeholder="provided by administrator"
    )

    st.markdown("""
    <div style="margin-top:8px;padding:8px 12px;
                border-left:2px solid #c9a84c;
                background:rgba(201,168,76,0.04);">
        <span style="font-family:'JetBrains Mono',monospace;
                     font-size:11px;color:#5c3d2e;">
            Access is strictly by invitation only.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    if st.button("Request Access →", key="signup_btn"):
        if not all([new_username, new_email, new_password, invite_code]):
            st.error("All fields required.")
        else:
            with st.spinner("Creating account..."):
                result = signup(
                    new_username, new_email,
                    new_password, invite_code
                )
            if result:
                st.session_state.boot_done = False
                st.rerun()
            else:
                st.error("Invalid invite code or credentials in use.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:20px;">
    <span style="font-family:'JetBrains Mono',monospace;
                 font-size:10px;color:#2c1810;
                 letter-spacing:0.1em;">
        PRIVATE PLATFORM · UNAUTHORIZED ACCESS PROHIBITED
    </span>
</div>
""", unsafe_allow_html=True)