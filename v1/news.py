"""
news.py — Cybersecurity news collector for SentinelAI.

Fetches articles from HackerNews Algolia API and RSS feeds.
Scrapes article body content for AI summarization.
Returns Article dataclass objects ready for storage.
"""

import requests
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from models import Article
from config import HACKERNEWS_API_URL, RSS_FEEDS, NEWS_FETCH_LIMIT


SECURITY_KEYWORDS = [
    "vulnerability", "exploit", "malware", "ransomware",
    "CVE", "patch", "breach", "zero-day", "phishing",
    "cybersecurity", "hacking", "threat", "attack"
]


def is_security_related(text: str) -> bool:
    """
    Check if text contains cybersecurity keywords.

    Args:
        text: Title or content to check.

    Returns:
        True if security related, False otherwise.
    """
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in SECURITY_KEYWORDS)


def scrape_article_content(url: str) -> str:
    """
    Scrape article body text from a URL.
    Strips scripts, styles, nav, and footer noise.
    Returns empty string on any failure.

    Args:
        url: Article URL to scrape.

    Returns:
        Cleaned article body text (max 3000 chars), or empty string.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Extract paragraph text
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        text = " ".join(text.split())  # Normalize whitespace

        return text[:3000]

    except requests.Timeout:
        print(f"[news.py] Scrape timeout for: {url}")
        return ""
    except requests.RequestException as e:
        print(f"[news.py] Scrape request failed for {url}: {e}")
        return ""
    except Exception as e:
        print(f"[news.py] Scrape failed for {url}: {e}")
        return ""


def fetch_hackernews() -> list[Article]:
    """
    Fetch cybersecurity stories from HackerNews Algolia API.
    No API key required.

    Returns:
        List of Article objects from HackerNews.
    """
    articles = []

    try:
        params = {
            "query": "cybersecurity hacking vulnerability",
            "tags": "story",
            "hitsPerPage": NEWS_FETCH_LIMIT,
        }
        response = requests.get(HACKERNEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for hit in data.get("hits", []):
            title = hit.get("title", "")
            url = hit.get("url", "")

            if not title or not url:
                continue
            if not is_security_related(title):
                continue

            published_at = datetime.utcfromtimestamp(
                hit.get("created_at_i", 0)
            )

            articles.append(Article(
                title=title,
                url=url,
                source="HackerNews",
                published_at=published_at,
            ))

    except requests.RequestException as e:
        print(f"[news.py] HackerNews fetch failed: {e}")

    return articles


def fetch_rss_feeds() -> list[Article]:
    """
    Fetch articles from RSS feeds defined in config.

    Returns:
        List of Article objects from all RSS feeds.
    """
    articles = []

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:20]:
                title = entry.get("title", "")
                url = entry.get("link", "")

                if not title or not url:
                    continue

                published_at = datetime.utcnow()
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_at = datetime(*entry.published_parsed[:6])

                # Use RSS description as fallback content
                description = entry.get("summary", "") or entry.get("description", "")

                articles.append(Article(
                    title=title,
                    url=url,
                    source=feed.feed.get("title", feed_url),
                    published_at=published_at,
                    raw_content=description,
                ))

        except Exception as e:
            print(f"[news.py] RSS feed failed {feed_url}: {e}")

    return articles


def collect_all_news() -> list[Article]:
    """
    Run all collectors, deduplicate, scrape content.

    Returns:
        List of unique Article objects with raw_content populated.
    """
    all_articles = []
    all_articles.extend(fetch_hackernews())
    all_articles.extend(fetch_rss_feeds())

    # Deduplicate by URL
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        if article.url not in seen_urls:
            seen_urls.add(article.url)
            unique_articles.append(article)

    # Scrape content for articles that don't have it yet
    for article in unique_articles:
        existing = getattr(article, "raw_content", "") or ""
        if len(existing.split()) < 30:
            scraped = scrape_article_content(article.url)
            if scraped:
                article.raw_content = scraped
            # If scrape also fails, raw_content stays as-is
            # ai.py will handle the empty content gracefully

    print(f"[news.py] Collected {len(unique_articles)} unique articles")
    return unique_articles