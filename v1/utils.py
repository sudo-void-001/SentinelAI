"""
utils.py — Shared helper functions for SentinelAI.

Small reusable utilities used across multiple modules.
"""

from datetime import datetime


def format_timestamp(dt: datetime) -> str:
    """
    Format a datetime object to readable string.

    Args:
        dt: datetime object to format.

    Returns:
        Formatted string like '2024-06-26 14:30 UTC'
    """
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to max length with ellipsis.

    Args:
        text: String to truncate.
        max_length: Maximum character length.

    Returns:
        Truncated string with '...' if needed.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."


def get_severity_emoji(severity: str) -> str:
    """
    Return emoji for a severity level.

    Args:
        severity: One of critical, high, medium, low.

    Returns:
        Matching emoji string.
    """
    mapping = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
    }
    return mapping.get(severity.lower(), "⚪")


def log(module: str, message: str) -> None:
    """
    Print a formatted log message with timestamp.

    Args:
        module: Name of the calling module.
        message: Log message content.
    """
    timestamp = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{module}] {message}")