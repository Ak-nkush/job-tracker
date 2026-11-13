import yaml

from sources import greenhouse, lever
from filters import match_level
from storage import init_db, is_empty, save_jobs

SOURCES = {
    "greenhouse": greenhouse,
    "lever": lever,
}

with open("config.yaml") as f:
    config = yaml.safe_load(f)

filters = config["filters"]

# 1. Fetch
all_jobs = []
for source_name, module in SOURCES.items():
    for company in config.get(source_name, []):
        jobs = module.get_jobs(company)
        all_jobs.extend(jobs)
        print(f"{source_name} | {company} | {len(jobs)}")

print(f"Total jobs: {len(all_jobs)}")

# 2. Tag each job with its tier (None if it doesn't match)
for j in all_jobs:
    j["tier"] = match_level(j, filters)

# 3. Save, and find out what is new
conn = init_db()
first_run = is_empty(conn)
new_jobs = save_jobs(conn, all_jobs)

if first_run:
    print(f"\nFirst run: saved {len(new_jobs)} jobs silently. No alerts.")
    new_matches = []
else:
    new_matches = [j for j in new_jobs if j["tier"]]

# 4. Report
strong = [j for j in new_matches if j["tier"] == "strong"]
possible = [j for j in new_matches if j["tier"] == "possible"]

print(f"\nNew jobs: {len(new_jobs)} | New strong: {len(strong)} | New possible: {len(possible)}")

print("\n--- NEW STRONG ---")
for j in strong:
    print(j["company"], "|", j["title"], "|", j["location"], "|", j["url"])

print("\n--- NEW POSSIBLE ---")
for j in possible:
    print(j["company"], "|", j["title"], "|", j["location"], "|", j["url"])