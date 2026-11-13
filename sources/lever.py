import requests
from datetime import datetime, timezone

BASE_URL = "https://api.lever.co/v0/postings/{company}?mode=json"


def fetch_jobs(company):
    url = BASE_URL.format(company=company)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.json()  # Lever returns a list directly
    except requests.RequestException as e:
        print(f"Failed to fetch {company}: {e}")
        return []


def normalize_job(raw, company):
    created = raw.get("createdAt")
    updated_at = (
        datetime.fromtimestamp(created / 1000, tz=timezone.utc).isoformat()
        if created else ""
    )
    return {
        "id": f"lever-{company}-{raw['id']}",
        "title": raw["text"],
        "company": company,
        "location": (raw.get("categories") or {}).get("location", ""),
        "url": raw["hostedUrl"],
        "source": "lever",
        "updated_at": updated_at,
    }


def get_jobs(company):
    raw_jobs = fetch_jobs(company)
    return [normalize_job(job, company) for job in raw_jobs]