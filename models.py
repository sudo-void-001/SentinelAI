"""
models.py — Data blueprints for SentinelAI.

Every piece of data that moves between modules is
defined here as a dataclass. This is the single
source of truth for what an Article and CVE look like.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Article:
    """Represents a cybersecurity news article."""

    title: str
    url: str
    source: str
    published_at: datetime
    summary: str = ""
    category: str = "general"
    severity: str = "low"
    raw_content: str = ""


@dataclass
class CVE:
    """Represents a CVE vulnerability record."""

    cve_id: str
    description: str
    cvss_score: float
    severity: str
    published_at: datetime
    is_exploited: bool = False
    affected_products: str = ""