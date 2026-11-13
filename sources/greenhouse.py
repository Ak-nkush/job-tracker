import requests

BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

def fetch_jobs(company):
    url = BASE_URL.format(company=company)
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data["jobs"]
    except requests.RequestException as e:
        print(f"Failed to fetch {company}: {e}")
        return []


def normalize_job(raw, company):
    return {
        "id": f"greenhouse-{company}-{raw['id']}",
        "title": raw["title"],
        "company": company,
        "location": (raw.get("location") or {}).get("name", ""),
        "url": raw["absolute_url"],
        "source": "greenhouse",
        "updated_at": raw.get("updated_at", ""),
    }


def get_jobs(company):
    raw_jobs = fetch_jobs(company)
    return [normalize_job(job, company) for job in raw_jobs]