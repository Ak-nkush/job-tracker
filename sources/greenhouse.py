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