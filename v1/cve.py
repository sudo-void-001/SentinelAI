"""
cve.py — CVE collector for SentinelAI.

Fetches vulnerabilities from NVD and CISA KEV APIs.
No API key required for either source.
"""

import requests
from datetime import datetime, timedelta
from models import CVE
from config import NVD_API_URL, CISA_KEV_URL, CVE_FETCH_LIMIT


def get_severity(cvss_score: float) -> str:
    """
    Convert CVSS score to severity label.

    Args:
        cvss_score: Numeric CVSS score 0.0 to 10.0.

    Returns:
        Severity string: critical, high, medium, or low.
    """
    if cvss_score >= 9.0:
        return "critical"
    elif cvss_score >= 7.0:
        return "high"
    elif cvss_score >= 4.0:
        return "medium"
    return "low"


def fetch_nvd_cves() -> list[CVE]:
    """
    Fetch recent CVEs from NVD API.
    Pulls last 7 days of vulnerabilities.
    No API key required.

    Returns:
        List of CVE objects from NVD.
    """
    cves = []

    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)

        params = {
            "pubStartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
            "pubEndDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
            "resultsPerPage": CVE_FETCH_LIMIT,
        }

        response = requests.get(NVD_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        for item in data.get("vulnerabilities", []):
            cve_data = item.get("cve", {})
            cve_id = cve_data.get("id", "")
            descriptions = cve_data.get("descriptions", [])
            description = next(
                (d["value"] for d in descriptions if d["lang"] == "en"), ""
            )

            # Extract CVSS score
            cvss_score = 0.0
            metrics = cve_data.get("metrics", {})
            if "cvssMetricV31" in metrics:
                cvss_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
            elif "cvssMetricV2" in metrics:
                cvss_score = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]

            published_str = cve_data.get("published", "")
            try:
                published_at = datetime.fromisoformat(published_str[:19])
            except ValueError:
                published_at = datetime.utcnow()

            cves.append(CVE(
                cve_id=cve_id,
                description=description,
                cvss_score=cvss_score,
                severity=get_severity(cvss_score),
                published_at=published_at,
            ))

    except requests.RequestException as e:
        print(f"[cve.py] NVD fetch failed: {e}")

    return cves


def fetch_cisa_kev() -> list[CVE]:
    """
    Fetch known exploited vulnerabilities from CISA KEV.
    These are CVEs actively exploited in the wild.
    No API key required.

    Returns:
        List of CVE objects marked as actively exploited.
    """
    cves = []

    try:
        response = requests.get(CISA_KEV_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        for vuln in data.get("vulnerabilities", [])[:CVE_FETCH_LIMIT]:
            cve_id = vuln.get("cveID", "")
            description = vuln.get("shortDescription", "")
            affected_products = vuln.get("product", "")

            published_str = vuln.get("dateAdded", "")
            try:
                published_at = datetime.strptime(published_str, "%Y-%m-%d")
            except ValueError:
                published_at = datetime.utcnow()

            cves.append(CVE(
                cve_id=cve_id,
                description=description,
                cvss_score=0.0,
                severity="high",
                published_at=published_at,
                is_exploited=True,
                affected_products=affected_products,
            ))

    except requests.RequestException as e:
        print(f"[cve.py] CISA KEV fetch failed: {e}")

    return cves


def collect_all_cves() -> list[CVE]:
    """
    Run all CVE collectors and return deduplicated results.

    Returns:
        List of unique CVE objects from all sources.
    """
    all_cves = []
    all_cves.extend(fetch_nvd_cves())
    all_cves.extend(fetch_cisa_kev())

    # Deduplicate by CVE ID
    seen_ids = set()
    unique_cves = []
    for cve in all_cves:
        if cve.cve_id not in seen_ids:
            seen_ids.add(cve.cve_id)
            unique_cves.append(cve)

    print(f"[cve.py] Collected {len(unique_cves)} unique CVEs")
    return unique_cves