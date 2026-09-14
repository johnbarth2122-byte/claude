import json
import os

import config
import sources
from notifier import notify_new_jobs


def load_seen():
    if os.path.exists(config.SEEN_JOBS_DB):
        with open(config.SEEN_JOBS_DB) as f:
            return set(json.load(f))
    return set()


def save_seen(seen_ids):
    with open(config.SEEN_JOBS_DB, "w") as f:
        json.dump(sorted(seen_ids), f)


def run():
    seen = load_seen()

    jobs = sources.fetch_all(
        config.KEYWORDS,
        greenhouse_companies=config.GREENHOUSE_COMPANIES,
        lever_companies=config.LEVER_COMPANIES,
    )
    print(f"Fetched {len(jobs)} matching jobs total.")

    new_jobs = [j for j in jobs if j["id"] not in seen]
    print(f"{len(new_jobs)} are new since last run.")

    notify_new_jobs(new_jobs)

    seen.update(j["id"] for j in jobs)
    save_seen(seen)


if __name__ == "__main__":
    run()
