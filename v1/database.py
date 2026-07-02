"""
database.py — SQLite storage layer for SentinelAI.

All database operations go through this file.
No other module should import sqlite3 directly.
"""

import sqlite3
from datetime import datetime
from config import DB_PATH
from models import Article, CVE


def get_connection() -> sqlite3.Connection:
    """
    Create and return a database connection.

    Returns:
        sqlite3.Connection with row_factory set for dict-like access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """
    Create all tables if they don't exist.
    Safe to run multiple times — won't overwrite data.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            published_at TEXT NOT NULL,
            summary TEXT DEFAULT '',
            category TEXT DEFAULT 'general',
            severity TEXT DEFAULT 'low',
            raw_content TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            cvss_score REAL DEFAULT 0.0,
            severity TEXT DEFAULT 'unknown',
            published_at TEXT NOT NULL,
            is_exploited INTEGER DEFAULT 0,
            affected_products TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_article(article: Article) -> bool:
    """
    Insert one article into the database.
    Skips duplicates silently using IGNORE.

    Args:
        article: Article dataclass object to store.

    Returns:
        True if inserted, False if duplicate skipped.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO articles
        (title, url, source, published_at, summary, category, severity, raw_content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        article.title,
        article.url,
        article.source,
        article.published_at.isoformat(),
        article.summary,
        article.category,
        article.severity,
        article.raw_content,
    ))

    inserted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return inserted


def insert_cve(cve: CVE) -> bool:
    """
    Insert one CVE into the database.
    Skips duplicates silently using IGNORE.

    Args:
        cve: CVE dataclass object to store.

    Returns:
        True if inserted, False if duplicate skipped.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO cves
        (cve_id, description, cvss_score, severity, published_at, is_exploited, affected_products)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        cve.cve_id,
        cve.description,
        cve.cvss_score,
        cve.severity,
        cve.published_at.isoformat(),
        int(cve.is_exploited),
        cve.affected_products,
    ))

    inserted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return inserted


def get_recent_articles(limit: int = 20) -> list[dict]:
    """
    Fetch most recent articles from database.

    Args:
        limit: Number of articles to return.

    Returns:
        List of article records as dictionaries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM articles
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_critical_cves() -> list[dict]:
    """
    Fetch all CVEs with CVSS score 9.0 or above.

    Returns:
        List of critical CVE records as dictionaries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM cves
        WHERE cvss_score >= 9.0
        ORDER BY cvss_score DESC
    """)

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows