"""
routers/dashboard.py — Dashboard data routes for SentinelAI V2.

Serves threat intelligence data to the Streamlit frontend.
All routes require authentication.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.auth_deps import get_current_user
from models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/articles")
def get_articles(
    limit: int = Query(default=20, le=100),
    severity: str = Query(default=None),
    category: str = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get latest cybersecurity articles.

    Args:
        limit: Max articles to return.
        severity: Filter by severity level.
        category: Filter by threat category.

    Returns:
        List of article dicts.
    """
    import sqlite3
    from pathlib import Path

    v1_db = Path(__file__).resolve().parent.parent.parent.parent / "v1" / "data" / "sentinel.db"

    if not v1_db.exists():
        return []

    conn = sqlite3.connect(str(v1_db))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM articles"
    params = []
    conditions = []

    if severity:
        conditions.append("severity = ?")
        params.append(severity)
    if category:
        conditions.append("category = ?")
        params.append(category)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


@router.get("/cves")
def get_cves(
    limit: int = Query(default=20, le=100),
    critical_only: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get latest CVEs.

    Args:
        limit: Max CVEs to return.
        critical_only: If True, return only CVSS 9.0+ CVEs.

    Returns:
        List of CVE dicts.
    """
    import sqlite3
    from pathlib import Path

    v1_db = Path(__file__).resolve().parent.parent.parent.parent / "v1" / "data" / "sentinel.db"

    if not v1_db.exists():
        return []

    conn = sqlite3.connect(str(v1_db))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if critical_only:
        cursor.execute(
            "SELECT * FROM cves WHERE cvss_score >= 9.0 ORDER BY cvss_score DESC LIMIT ?",
            (limit,)
        )
    else:
        cursor.execute(
            "SELECT * FROM cves ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard statistics for the current user.

    Returns:
        Dict with article and CVE counts by severity.
    """
    import sqlite3
    from pathlib import Path

    v1_db = Path(__file__).resolve().parent.parent.parent.parent / "v1" / "data" / "sentinel.db"

    if not v1_db.exists():
        return {
            "total_articles": 0,
            "total_cves": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

    conn = sqlite3.connect(str(v1_db))
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles")
    total_articles = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM cves")
    total_cves = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM articles WHERE severity='critical'")
    critical = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM articles WHERE severity='high'")
    high = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM articles WHERE severity='medium'")
    medium = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM articles WHERE severity='low'")
    low = cursor.fetchone()[0]

    conn.close()

    return {
        "total_articles": total_articles,
        "total_cves": total_cves,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "username": current_user.username,
        "digest_slot": current_user.digest_slot,
    }