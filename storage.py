import sqlite3
from datetime import datetime, timezone


def init_db(path="jobs.db"):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id          TEXT PRIMARY KEY,
            title       TEXT,
            company     TEXT,
            location    TEXT,
            url         TEXT,
            source      TEXT,
            updated_at  TEXT,
            tier        TEXT,
            first_seen  TEXT
        )
    """)
    conn.commit()
    return conn


def is_empty(conn):
    return conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 0


def save_jobs(conn, jobs):
    """Insert jobs. Return only the ones that were not in the database before."""
    now = datetime.now(timezone.utc).isoformat()
    new_jobs = []
    for j in jobs:
        cur = conn.execute(
            """INSERT OR IGNORE INTO jobs
               (id, title, company, location, url, source, updated_at, tier, first_seen)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (j["id"], j["title"], j["company"], j["location"], j["url"],
             j["source"], j["updated_at"], j["tier"], now),
        )
        if cur.rowcount == 1:
            new_jobs.append(j)
    conn.commit()
    return new_jobs