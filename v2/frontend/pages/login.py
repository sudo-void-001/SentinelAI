"""
pages/login.py — Login and signup pages for SentinelAI V2.

Login: centered, clean cream luxury.
Signup: dark immersive — user should be shocked by the contrast
when they enter the cream dashboard.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components.theme import apply_theme
from components.api_client import login, signup

st.set_page_config(
    page_title="SentinelAI — Access",
    page_icon="🛡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Override to hide sidebar completely on this page
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="collapsedControl"] {display: none !important;}
.stApp > header {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stSidebarNav"] {display: none !important;}

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --gold: #c9a84c;
    --gold-dark: #a8873a;
    --cream: #f5f0e8;
    --parchment: #ede8dc;
    --border: #d4c4a0;
    --brown-deep: #2c1810;
    --brown-mid: #5c3d2e;
    --brown-muted: #8b6f47;
    --espresso: #1a1008;
    --espresso-mid: #2c1810;
    --espresso-light: #3d2510;
}

.stApp {
    background-color: var(--cream) !important;
    font-family: 'Inter', sans-serif !important;
}

.main .block-container {
    background-color: transparent !important;
    padding-top: 0 !important;
    max-width: 480px !important;
}

.stTextInput input {
    background-color: var(--parchment) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--brown-deep) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 10px 14px !important;
    font-size: 13px !important;
}

.stTextInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}

.stTextInput label {
    color: var(--brown-muted) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

.stButton button {
    background: linear-gradient(135deg, #c9a84c 0%, #a8873a 100%) !important;
    color: #1a1008 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    letter-spacing: 0.04em !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(201,168,76,0.3) !important;
    width: 100% !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.4) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: var(--brown-muted) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
}

.stTabs [aria-selected="true"] {
    color: var(--gold-dark) !important;
    border-bottom: 2px solid var(--gold) !important;
    background-color: transparent !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

if st.session_state.get("token"):
    st.switch_page("pages/dashboard.py")

# Determine which tab to show
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# ─── LOGIN PAGE ───────────────────────────────────
if not st.session_state.show_signup:

    st.markdown("""
    <div style="min-height:100vh;display:flex;flex-direction:column;
                justify-content:center;padding:40px 0;">

        <div style="text-align:center;margin-bottom:32px;">
            <div style="font-family:'Playfair Display',serif;
                        font-size:38px;font-weight:700;
                        color:#2c1810;letter-spacing:0.02em;
                        margin-bottom:10px;">
                SentinelAI
            </div>
            <div style="width:48px;height:1px;
                        background:linear-gradient(90deg,transparent,#c9a84c,transparent);
                        margin:0 auto 12px auto;">
            </div>
            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:10px;color:#8b6f47;
                        letter-spacing:0.18em;text-transform:uppercase;">
                Cyber Threat Intelligence Platform
            </div>
        </div>

        <div style="background:#ede8dc;border:1px solid #d4c4a0;
                    border-radius:10px;padding:32px;
                    box-shadow:0 4px 24px rgba(44,24,16,0.08);">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Playfair Display',serif;
                font-size:18px;font-weight:600;
                color:#2c1810;margin-bottom:20px;">
        Sign In
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div style="text-align:center;margin-top:20px;
                padding-top:20px;border-top:1px solid #d4c4a0;">
        <div style="font-family:'JetBrains Mono',monospace;
                    font-size:11px;color:#8b6f47;margin-bottom:8px;">
            Have an invite code?
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Create Account →", key="go_signup"):
        st.session_state.show_signup = True
        st.rerun()

    st.markdown("""
        </div>
        <div style="text-align:center;margin-top:20px;">
            <span style="font-family:'JetBrains Mono',monospace;
                         font-size:10px;color:#b8a882;
                         letter-spacing:0.08em;">
                PRIVATE PLATFORM · INVITE ONLY
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── SIGNUP PAGE ──────────────────────────────────
else:
    # Dark immersive signup — contrast shock when entering dashboard
    st.markdown("""
    <style>
    .stApp {
        background-color: #0d0a06 !important;
    }
    .main .block-container {
        background-color: transparent !important;
    }
    .stTextInput input {
        background-color: #1a1008 !important;
        border: 1px solid #3d2510 !important;
        color: #e8d5a3 !important;
    }
    .stTextInput input:focus {
        border-color: #c9a84c !important;
    }
    .stTextInput input::placeholder {
        color: #5c3d2e !important;
    }
    .stTextInput label {
        color: #8b6f47 !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #c9a84c, #a8873a) !important;
        color: #0d0a06 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="min-height:100vh;display:flex;
                flex-direction:column;justify-content:center;
                padding:40px 0;">

        <div style="text-align:center;margin-bottom:32px;">
            <div style="font-family:'Playfair Display',serif;
                        font-size:36px;font-weight:700;
                        color:#c9a84c;letter-spacing:0.02em;
                        margin-bottom:10px;">
                SentinelAI
            </div>
            <div style="width:48px;height:1px;
                        background:linear-gradient(90deg,transparent,#c9a84c,transparent);
                        margin:0 auto 12px auto;">
            </div>
            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:10px;color:#5c3d2e;
                        letter-spacing:0.18em;text-transform:uppercase;">
                Create Your Account
            </div>
        </div>

        <div style="background:#1a1008;
                    border:1px solid #3d2510;
                    border-radius:10px;padding:32px;
                    box-shadow:0 8px 40px rgba(0,0,0,0.5);">

            <div style="font-family:'Playfair Display',serif;
                        font-size:18px;font-weight:600;
                        color:#e8d5a3;margin-bottom:6px;">
                Request Access
            </div>
            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:11px;color:#5c3d2e;
                        margin-bottom:24px;letter-spacing:0.04em;">
                You'll need a valid invite code to proceed.
            </div>
    """, unsafe_allow_html=True)

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
    <div style="margin-top:8px;padding:10px 12px;
                background:rgba(201,168,76,0.06);
                border:1px solid #3d2510;border-radius:5px;
                border-left:2px solid #c9a84c;">
        <span style="font-family:'JetBrains Mono',monospace;
                     font-size:11px;color:#8b6f47;">
            Access is strictly by invitation.
            Contact the administrator for a code.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

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

    st.markdown("""
        </div>

        <div style="text-align:center;margin-top:16px;">
    """, unsafe_allow_html=True)

    if st.button("← Back to Sign In", key="back_login"):
        st.session_state.show_signup = False
        st.rerun()

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)