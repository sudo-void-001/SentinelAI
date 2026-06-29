"""
ai.py — AI intelligence layer for SentinelAI.

Uses official Groq SDK for summarization,
categorization, and severity estimation.
"""

from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL


# Phrases that indicate LLM received empty/missing content
FALLBACK_PHRASES = [
    "i'm missing the article",
    "i am missing the article",
    "could you provide the text",
    "i need the article",
    "please provide",
    "i don't have the article",
    "i do not have the article",
    "provide the article",
    "i cannot summarize",
    "no content provided",
    "missing the content",
    "article content",
    "provide the content",
    "share the article",
    "paste the article",
]

FALLBACK_SUMMARY = 'Summary unavailable.\nUse "Read more" to view the complete article.'

MIN_CONTENT_WORDS = 30


def get_client() -> Groq:
    """Return configured Groq client."""
    return Groq(api_key=GROQ_API_KEY)


def is_llm_fallback(text: str) -> bool:
    """
    Detect if LLM returned an internal fallback response
    instead of a real summary.

    Args:
        text: LLM response text.

    Returns:
        True if response is a fallback/internal message.
    """
    lowered = text.lower()
    return any(phrase in lowered for phrase in FALLBACK_PHRASES)


def has_sufficient_content(content: str) -> bool:
    """
    Validate that content has enough text to summarize.

    Args:
        content: Article body text.

    Returns:
        True if content meets minimum word threshold.
    """
    if not content or not content.strip():
        return False
    return len(content.split()) >= MIN_CONTENT_WORDS


def query_groq(prompt: str) -> str:
    """
    Send a prompt to Groq and return response.

    Args:
        prompt: Instruction and content to process.

    Returns:
        AI response text, or empty string on failure.
    """
    if not GROQ_API_KEY:
        print("[ai.py] No GROQ_API_KEY found in .env")
        return ""

    try:
        client = get_client()
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ai.py] Groq call failed: {e}")
        return ""


def summarize_article(title: str, content: str) -> str:
    """
    Generate a 2-sentence summary of an article.
    Validates content before sending to LLM.
    Rejects LLM fallback responses.

    Args:
        title: Article headline.
        content: Article body or description.

    Returns:
        2-sentence AI summary string, or safe fallback message.
    """
    # Validate content before hitting the API
    if not has_sufficient_content(content):
        print(f"[ai.py] Insufficient content ({len(content.split()) if content else 0} words) for: {title}")
        return FALLBACK_SUMMARY

    prompt = f"""You are a cybersecurity analyst.
Summarize this article in exactly 2 sentences.
Be technical and precise. No fluff.
Do NOT ask for more information. Summarize only what is provided.

Title: {title}
Content: {content[:3000]}

Summary:"""

    result = query_groq(prompt)

    # Reject empty responses
    if not result or not result.strip():
        print(f"[ai.py] Empty LLM response for: {title}")
        return FALLBACK_SUMMARY

    # Reject LLM fallback/internal messages
    if is_llm_fallback(result):
        print(f"[ai.py] LLM returned fallback response for: {title}")
        print(f"[ai.py] Rejected response was: {result[:100]}")
        return FALLBACK_SUMMARY

    return result


def categorize_article(title: str) -> str:
    """
    Categorize an article into a threat type.

    Args:
        title: Article headline.

    Returns:
        Category string.
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
    Estimate threat severity.

    Args:
        title: Article headline.
        summary: AI-generated summary.

    Returns:
        Severity string: critical, high, medium, or low.
    """
    # If summary is a fallback, estimate from title only
    if summary == FALLBACK_SUMMARY:
        summary = "No summary available."

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

    Args:
        title: Article headline.
        content: Article body or description.

    Returns:
        Dict with summary, category, severity.
    """
    summary = summarize_article(title, content)
    category = categorize_article(title)
    severity = estimate_severity(title, summary)

    return {
        "summary": summary,
        "category": category,
        "severity": severity,
    }