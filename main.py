import yaml

from sources import greenhouse, lever
from filters import match_level

SOURCES = {
    "greenhouse": greenhouse,
    "lever": lever,
}

with open("config.yaml") as f:
    config = yaml.safe_load(f)

all_jobs = []

for source_name, module in SOURCES.items():
    for company in config.get(source_name, []):
        jobs = module.get_jobs(company)
        all_jobs.extend(jobs)
        print(f"{source_name} | {company} | {len(jobs)}")

print(f"Total jobs: {len(all_jobs)}")

filters = config["filters"]
strong = [j for j in all_jobs if match_level(j, filters) == "strong"]
possible = [j for j in all_jobs if match_level(j, filters) == "possible"]

print(f"\nStrong: {len(strong)} | Possible: {len(possible)} | Total: {len(all_jobs)}")

print("\n--- STRONG ---")
for j in strong:
    print(j["company"], "|", j["title"], "|", j["location"])

print("\n--- POSSIBLE ---")
for j in possible[:20]:
    print(j["company"], "|", j["title"], "|", j["location"])