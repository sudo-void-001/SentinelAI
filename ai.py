"""
ai.py — AI intelligence layer for SentinelAI.

Connects to Groq API to summarize articles,
categorize threats, and estimate severity.
Model: llama3-8b-8192 (free tier)
"""

import requests
from config import GROQ_API_KEY, GROQ_MODEL


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def query_groq(prompt: str) -> str:
    """
    Send a prompt to Groq API and return the response.

    Args:
        prompt: The instruction and content to process.

    Returns:
        AI response text, or empty string on failure.
    """
    if not GROQ_API_KEY:
        print("[ai.py] No GROQ_API_KEY found in .env")
        return ""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.3,
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.RequestException as e:
        print(f"[ai.py] Groq API call failed: {e}")
        return ""


def summarize_article(title: str, content: str) -> str:
    """
    Generate a 2-sentence summary of an article.

    Args:
        title: Article headline.
        content: Article body or description.

    Returns:
        2-sentence AI summary string.
    """
    prompt = f"""You are a cybersecurity analyst.
Summarize this article in exactly 2 sentences.
Be technical and precise. No fluff.

Title: {title}
Content: {content}

Summary:"""

    return query_groq(prompt)


def categorize_article(title: str) -> str:
    """
    Categorize an article into a threat type.

    Args:
        title: Article headline.

    Returns:
        Category string: ransomware, vulnerability, breach,
        malware, patch, phishing, or general.
    """
    prompt = f"""Categorize this cybersecurity headline into exactly one word.
Choose from: ransomware, vulnerability, breach, malware, patch, phishing, general

Headline: {title}

Category:"""

    result = query_groq(prompt).lower().strip()
    valid = {"ransomware", "vulnerability", "breach", "malware", "patch", "phishing", "general"}
    return result if result in valid else "general"


def estimate_severity(title: str, summary: str) -> str:
    """
    Estimate threat severity from title and summary.

    Args:
        title: Article headline.
        summary: AI-generated summary.

    Returns:
        Severity string: critical, high, medium, or low.
    """
    prompt = f"""Rate the severity of this cybersecurity threat.
Reply with exactly one word: critical, high, medium, or low.

Title: {title}
Summary: {summary}

Severity:"""

    result = query_groq(prompt).lower().strip()
    valid = {"critical", "high", "medium", "low"}
    return result if result in valid else "low"


def enrich_article(title: str, content: str) -> dict:
    """
    Run all AI functions on one article.
    Returns summary, category, and severity together.

    Args:
        title: Article headline.
        content: Article body or description.

    Returns:
        Dict with keys: summary, category, severity.
    """
    summary = summarize_article(title, content)
    category = categorize_article(title)
    severity = estimate_severity(title, summary)

    return {
        "summary": summary,
        "category": category,
        "severity": severity,
    }