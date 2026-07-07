"""
pages/settings.py — User settings page.
Luxury Bloomberg Terminal aesthetic.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components.theme import apply_theme, card, page_header, sidebar_nav
from components.api_client import get_available_slots, select_slot

st.set_page_config(
    page_title="SentinelAI — Settings",
    page_icon="⚙️",
    layout="wide",
)

apply_theme()

if not st.session_state.get("token"):
    st.switch_page("pages/login.py")

username = st.session_state.get("username", "")
role = st.session_state.get("role", "user")

sidebar_nav(username, role)

page_header("Settings", "Preferences and digest schedule")

# ─── DIGEST SLOT ──────────────────────────────────
st.markdown("""
<div class="section-label">📅 Daily Digest Schedule</div>
""", unsafe_allow_html=True)

card("""
<div style="font-size:13px;color:#5c3d2e;margin-bottom:8px;
            line-height:1.6;">
    Choose your preferred time to receive the daily threat
    intelligence digest. Each slot is exclusive — once claimed,
    no other user may select it.
</div>
<div style="font-family:'JetBrains Mono',monospace;font-size:11px;
            color:#b8a882;">
    The 9:00 AM slot is permanently reserved for the administrator.
</div>
""")

slots = get_available_slots()

if slots:
    available = [
        s for s in slots
        if s.get("available") and not s.get("is_admin_slot")
    ]
    your_slot = next((s for s in slots if s.get("is_yours")), None)

    if your_slot:
        st.markdown(f"""
        <div style="background:rgba(39,174,96,0.08);
                    border:1px solid rgba(39,174,96,0.2);
                    border-radius:6px;padding:10px 14px;
                    margin-bottom:16px;">
            <span style="font-family:'JetBrains Mono',monospace;
                         font-size:12px;color:#27ae60;">
                ✓ Your current digest time:
                <strong>{your_slot['label']} IST</strong>
            </span>
        </div>
        """, unsafe_allow_html=True)

    if available:
        slot_options = {s["label"]: s["hour"] for s in available}
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_label = st.selectbox(
                "Select Digest Time (IST)",
                options=list(slot_options.keys()),
                key="slot_select"
            )
        with col2:
            st.markdown("<div style='height:28px;'></div>",
                       unsafe_allow_html=True)
            if st.button("Save →", key="save_slot"):
                hour = slot_options[selected_label]
                if select_slot(hour):
                    st.success(f"Digest scheduled for {selected_label}")
                    st.rerun()
                else:
                    st.error("Slot unavailable. Please choose another.")
    else:
        st.markdown("""
        <div style="background:rgba(192,57,43,0.08);
                    border:1px solid rgba(192,57,43,0.15);
                    border-radius:6px;padding:10px 14px;">
            <span style="font-family:'JetBrains Mono',monospace;
                         font-size:12px;color:#c0392b;">
                All time slots are currently assigned.
            </span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─── ACCOUNT ──────────────────────────────────────
st.markdown("""
<div class="section-label">👤 Account</div>
""", unsafe_allow_html=True)

card(f"""
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;">
    <div>
        <div style="font-size:10px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:6px;">Username</div>
        <div style="font-size:15px;color:#2c1810;font-weight:600;">
            {username}
        </div>
    </div>
    <div>
        <div style="font-size:10px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:6px;">Role</div>
        <div style="font-size:15px;color:#a8873a;font-weight:600;
                    font-family:'JetBrains Mono',monospace;">
            {role.upper()}
        </div>
    </div>
    <div>
        <div style="font-size:10px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:6px;">Access Level</div>
        <div style="font-size:15px;color:#27ae60;font-weight:600;
                    font-family:'JetBrains Mono',monospace;">
            ACTIVE
        </div>
    </div>
</div>
""")

st.markdown("<hr>", unsafe_allow_html=True)

# ─── PLATFORM INFO ────────────────────────────────
st.markdown("""
<div class="section-label">ℹ️ Platform</div>
""", unsafe_allow_html=True)

card("""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:24px;">
    <div>
        <div style="font-size:10px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:6px;">Version</div>
        <div style="font-size:13px;color:#2c1810;
                    font-family:'JetBrains Mono',monospace;">
            V2.0.0
        </div>
    </div>
    <div>
        <div style="font-size:10px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:6px;">Access</div>
        <div style="font-size:13px;color:#a8873a;
                    font-family:'JetBrains Mono',monospace;">
            Invite Only
        </div>
    </div>
    <div>
        <div style="font-size:10px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:6px;">Capacity</div>
        <div style="font-size:13px;color:#2c1810;
                    font-family:'JetBrains Mono',monospace;">
            10 Users
        </div>
    </div>
    <div>
        <div style="font-size:10px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-bottom:6px;">Status</div>
        <div style="font-size:13px;color:#27ae60;
                    font-family:'JetBrains Mono',monospace;">
            Online
        </div>
    </div>
</div>
""")