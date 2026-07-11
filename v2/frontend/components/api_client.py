"""
components/api_client.py — HTTP client for SentinelAI V2.
"""

import os
import requests
import streamlit as st
from typing import Optional

# Use environment variable for production, fallback to local
API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def get_headers() -> dict:
    """
    Get authorization headers using stored token.

    Returns:
        Dict with Authorization header if token exists.
    """
    token = st.session_state.get("token", "")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def login(username: str, password: str) -> Optional[dict]:
    """
    Login and store token in session state.

    Args:
        username: User's username.
        password: User's password.

    Returns:
        Response dict on success, None on failure.
    """
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["username"] = data["username"]
            st.session_state["role"] = data["role"]
            return data
        return None
    except Exception:
        return None


def signup(username: str, email: str, password: str, invite_code: str) -> Optional[dict]:
    """
    Register a new user.

    Args:
        username: Desired username.
        email: User email address.
        password: Desired password.
        invite_code: Valid invite code from admin.

    Returns:
        Response dict on success, None on failure.
    """
    try:
        response = requests.post(
            f"{API_BASE}/auth/signup",
            json={
                "username": username,
                "email": email,
                "password": password,
                "invite_code": invite_code,
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["username"] = data["username"]
            st.session_state["role"] = data["role"]
            return data
        return None
    except Exception:
        return None


def get_articles(limit: int = 20, severity: str = None, category: str = None) -> list:
    """
    Fetch latest articles from backend.

    Args:
        limit: Max articles to fetch.
        severity: Optional severity filter.
        category: Optional category filter.

    Returns:
        List of article dicts.
    """
    try:
        params = {"limit": limit}
        if severity:
            params["severity"] = severity
        if category:
            params["category"] = category

        response = requests.get(
            f"{API_BASE}/dashboard/articles",
            headers=get_headers(),
            params=params,
            timeout=10
        )
        return response.json() if response.status_code == 200 else []
    except Exception:
        return []


def get_cves(limit: int = 20, critical_only: bool = False) -> list:
    """
    Fetch latest CVEs from backend.

    Args:
        limit: Max CVEs to fetch.
        critical_only: If True, return only critical CVEs.

    Returns:
        List of CVE dicts.
    """
    try:
        response = requests.get(
            f"{API_BASE}/dashboard/cves",
            headers=get_headers(),
            params={"limit": limit, "critical_only": critical_only},
            timeout=10
        )
        return response.json() if response.status_code == 200 else []
    except Exception:
        return []


def get_stats() -> dict:
    """
    Fetch dashboard statistics.

    Returns:
        Stats dict with article and CVE counts.
    """
    try:
        response = requests.get(
            f"{API_BASE}/dashboard/stats",
            headers=get_headers(),
            timeout=10
        )
        return response.json() if response.status_code == 200 else {}
    except Exception:
        return {}


def get_available_slots() -> list:
    """
    Fetch available digest time slots.

    Returns:
        List of slot dicts.
    """
    try:
        response = requests.get(
            f"{API_BASE}/slots/available",
            headers=get_headers(),
            timeout=10
        )
        return response.json() if response.status_code == 200 else []
    except Exception:
        return []


def select_slot(hour: int) -> bool:
    """
    Select a digest time slot.

    Args:
        hour: Hour (IST) to select.

    Returns:
        True if successful, False otherwise.
    """
    try:
        response = requests.post(
            f"{API_BASE}/slots/select/{hour}",
            headers=get_headers(),
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False


def get_admin_stats() -> dict:
    """Fetch admin platform statistics."""
    try:
        response = requests.get(
            f"{API_BASE}/admin/stats",
            headers=get_headers(),
            timeout=10
        )
        return response.json() if response.status_code == 200 else {}
    except Exception:
        return {}


def get_all_users() -> list:
    """Fetch all users (admin only)."""
    try:
        response = requests.get(
            f"{API_BASE}/admin/users",
            headers=get_headers(),
            timeout=10
        )
        return response.json() if response.status_code == 200 else []
    except Exception:
        return []


def disable_user(user_id: int) -> bool:
    """Disable a user account (admin only)."""
    try:
        response = requests.post(
            f"{API_BASE}/admin/users/{user_id}/disable",
            headers=get_headers(),
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False


def enable_user(user_id: int) -> bool:
    """Enable a user account (admin only)."""
    try:
        response = requests.post(
            f"{API_BASE}/admin/users/{user_id}/enable",
            headers=get_headers(),
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False


def create_invite() -> Optional[str]:
    """Generate a new invite code (admin only)."""
    try:
        response = requests.post(
            f"{API_BASE}/admin/invites/create",
            headers=get_headers(),
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("invite_code")
        return None
    except Exception:
        return None


def logout() -> None:
    """Clear session state to log out."""
    for key in ["token", "username", "role"]:
        st.session_state.pop(key, None)