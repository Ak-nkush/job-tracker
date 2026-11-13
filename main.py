from sources.greenhouse import fetch_jobs

jobs = fetch_jobs("stripe")
print(f"Found {len(jobs)} jobs")

for job in jobs[:10]:
    print(job["title"], "|", job["location"]["name"])