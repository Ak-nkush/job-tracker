import yaml
from filters import is_match

with open("config.yaml") as f:
    filters = yaml.safe_load(f)["filters"]


def job(title, location):
    return {"title": title, "location": location}


# (job, expected result)
cases = [
    (job("Software Engineer Intern", "Bengaluru, India"), True),
    (job("Graduate Engineer Trainee", "Pune"), True),
    (job("Junior Data Analyst", "Remote - India"), True),
    (job("Software Engineer, SDE-1", "Hyderabad"), True),
    (job("Senior Software Engineer", "Bengaluru"), False),
    (job("Software Engineer Intern", "New York"), False),
    (job("Internal Tools Engineer", "Mumbai"), False),
    (job("Sales Associate", "Delhi"), False),
]

for j, expected in cases:
    result = is_match(j, filters)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status} | {j['title']} | {j['location']} | got {result}, expected {expected}")