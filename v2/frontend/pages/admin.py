"""
pages/admin.py — Admin control panel.
Luxury Bloomberg Terminal aesthetic.
"""

import streamlit as st
import sys
import requests
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components.theme import apply_theme, card, page_header, sidebar_nav
from components.api_client import (
    get_admin_stats, get_all_users,
    disable_user, enable_user,
    create_invite, get_headers, logout
)

st.set_page_config(
    page_title="SentinelAI — Admin",
    page_icon="🔧",
    layout="wide",
)

apply_theme()

if not st.session_state.get("token"):
    st.switch_page("pages/login.py")

if st.session_state.get("role") != "admin":
    st.error("Access restricted to administrators.")
    st.stop()

username = st.session_state.get("username", "")
role = st.session_state.get("role", "user")

sidebar_nav(username, role)

page_header("Admin Panel", "Platform management and oversight")

# ─── STATS ────────────────────────────────────────
stats = get_admin_stats()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(
        "Platform Users",
        f"{stats.get('total_users', 0)} / 10"
    )
with c2:
    st.metric("Active", stats.get("active_users", 0))
with c3:
    st.metric("Invites Used", stats.get("used_invites", 0))
with c4:
    st.metric(
        "System",
        stats.get("system_status", "unknown").upper()
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "User Management",
    "Invite Codes",
    "Digest Schedule"
])

# ─── TAB 1 ────────────────────────────────────────
with tab1:
    users = get_all_users()

    if not users:
        st.markdown("""
        <div style="text-align:center;padding:48px;
                    color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;">
            No users registered.
        </div>
        """, unsafe_allow_html=True)
    else:
        for user in users:
            user_id = user.get("id")
            uname = user.get("username", "")
            email = user.get("email", "")
            urole = user.get("role", "user")
            is_active = user.get("is_active", True)
            digest_slot = user.get("digest_slot")
            slot_label = f"{digest_slot}:00 IST" if digest_slot else "—"

            status_color = "#27ae60" if is_active else "#c0392b"
            status_text = "Active" if is_active else "Disabled"

            col1, col2 = st.columns([5, 1])

            with col1:
                card(f"""
                <div style="display:flex;align-items:center;
                            justify-content:space-between;">
                    <div style="display:flex;
                                align-items:center;gap:12px;">
                        <div style="width:36px;height:36px;
                                    background:rgba(201,168,76,0.15);
                                    border:1px solid #d4c4a0;
                                    border-radius:6px;
                                    display:flex;align-items:center;
                                    justify-content:center;
                                    font-weight:700;color:#a8873a;
                                    font-size:15px;
                                    font-family:'Playfair Display',serif;">
                            {uname[0].upper()}
                        </div>
                        <div>
                            <div style="font-size:14px;font-weight:600;
                                        color:#2c1810;">{uname}</div>
                            <div style="font-size:11px;color:#8b6f47;
                                        font-family:'JetBrains Mono',monospace;">
                                {email}
                            </div>
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;align-items:center;">
                        <span style="background:rgba(44,24,16,0.06);
                                     color:#8b6f47;padding:2px 8px;
                                     border-radius:3px;font-size:10px;
                                     font-family:'JetBrains Mono',monospace;
                                     text-transform:uppercase;
                                     letter-spacing:0.04em;">
                            📅 {slot_label}
                        </span>
                        <span style="background:rgba(44,24,16,0.06);
                                     color:#8b6f47;padding:2px 8px;
                                     border-radius:3px;font-size:10px;
                                     font-family:'JetBrains Mono',monospace;
                                     text-transform:uppercase;">
                            {urole}
                        </span>
                        <span style="color:{status_color};
                                     font-size:11px;font-weight:600;
                                     font-family:'JetBrains Mono',monospace;">
                            ● {status_text}
                        </span>
                    </div>
                </div>
                """)

            with col2:
                if urole != "admin":
                    if is_active:
                        if st.button(
                            "Disable",
                            key=f"dis_{user_id}"
                        ):
                            if disable_user(user_id):
                                st.rerun()
                    else:
                        if st.button(
                            "Enable",
                            key=f"en_{user_id}"
                        ):
                            if enable_user(user_id):
                                st.rerun()

# ─── TAB 2 ────────────────────────────────────────
with tab2:
    col1, col2 = st.columns([3, 1])

    with col2:
        if st.button("Generate Code →", key="gen_invite"):
            new_code = create_invite()
            if new_code:
                st.success(f"`{new_code}`")
            else:
                st.error("Failed.")

    with col1:
        st.markdown("""
        <div style="font-size:12px;color:#8b6f47;
                    font-family:'JetBrains Mono',monospace;
                    margin-bottom:8px;">
            Each code grants one-time access to a new user.
        </div>
        """, unsafe_allow_html=True)

    try:
        response = requests.get(
            "http://127.0.0.1:8000/admin/invites",
            headers=get_headers(),
            timeout=10
        )
        invites = response.json() if response.status_code == 200 else []
    except Exception:
        invites = []

    for invite in invites:
        code = invite.get("code", "")
        is_used = invite.get("is_used", False)
        status_color = "#b8a882" if is_used else "#27ae60"
        status_text = "Used" if is_used else "Available"

        card(f"""
        <div style="display:flex;align-items:center;
                    justify-content:space-between;">
            <span style="font-family:'JetBrains Mono',monospace;
                         font-size:13px;color:#2c1810;
                         letter-spacing:0.06em;">
                {code}
            </span>
            <span style="color:{status_color};
                         font-size:11px;font-weight:600;
                         font-family:'JetBrains Mono',monospace;">
                ● {status_text}
            </span>
        </div>
        """)

# ─── TAB 3 ────────────────────────────────────────
with tab3:
    users = get_all_users()
    all_slots = [6, 7, 8, 9, 10, 11, 12]
    labels = {
        6: "6:00 AM", 7: "7:00 AM", 8: "8:00 AM",
        9: "9:00 AM", 10: "10:00 AM",
        11: "11:00 AM", 12: "12:00 PM"
    }

    slot_map = {}
    for user in users:
        slot = user.get("digest_slot")
        if slot:
            slot_map[slot] = user.get("username")

    for hour in all_slots:
        label = labels[hour]
        assigned = slot_map.get(hour)
        is_admin_slot = hour == 9

        if assigned:
            color = "#a8873a" if is_admin_slot else "#2471a3"
            tag = "Admin Reserved" if is_admin_slot else "Assigned"
            card(f"""
            <div style="display:flex;align-items:center;
                        justify-content:space-between;">
                <span style="font-family:'JetBrains Mono',monospace;
                             font-size:13px;color:#2c1810;
                             font-weight:600;">
                    {label}
                </span>
                <div style="display:flex;gap:10px;align-items:center;">
                    <span style="font-size:13px;color:#5c3d2e;">
                        {assigned}
                    </span>
                    <span style="color:{color};font-size:11px;
                                 font-weight:600;
                                 font-family:'JetBrains Mono',monospace;">
                        ● {tag}
                    </span>
                </div>
            </div>
            """, variant="gold" if is_admin_slot else "blue")
        else:
            card(f"""
            <div style="display:flex;align-items:center;
                        justify-content:space-between;">
                <span style="font-family:'JetBrains Mono',monospace;
                             font-size:13px;color:#b8a882;">
                    {label}
                </span>
                <span style="color:#b8a882;font-size:11px;
                             font-family:'JetBrains Mono',monospace;">
                    Available
                </span>
            </div>
            """)