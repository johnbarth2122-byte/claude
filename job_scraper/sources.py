"""
Job source connectors.

Direct HTML scraping of LinkedIn/Indeed is intentionally NOT included here —
both sites actively fingerprint and block scrapers (login walls, rotating
markup, IP bans), which is almost certainly why "the scraper" was breaking.
Instead this pulls from sources that publish stable, public JSON:

- RemoteOK        (public JSON API, no key needed)
- Arbeitnow       (public JSON API, no key needed)
- Greenhouse      (per-company public JSON API — add your target companies)
- Lever           (per-company public JSON API — add your target companies)

This covers "all" the major sources that can actually be scraped reliably.
"""
import requests

USER_AGENT = "Mozilla/5.0 (compatible; JobAlertBot/1.0)"
TIMEOUT = 15


def _get_json(url, params=None):
    resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fetch_remoteok(keywords):
    """https://remoteok.com/api - public, no auth."""
    jobs = []
    try:
        data = _get_json("https://remoteok.com/api")
    except requests.RequestException as e:
        print(f"[remoteok] fetch failed: {e}")
        return jobs

    for item in data:
        if not isinstance(item, dict) or "id" not in item:
            continue
        text = f"{item.get('position', '')} {item.get('description', '')} {' '.join(item.get('tags', []))}".lower()
        if not keywords or any(k.lower() in text for k in keywords):
            jobs.append({
                "id": f"remoteok_{item['id']}",
                "title": item.get("position", "Unknown"),
                "company": item.get("company", "Unknown"),
                "location": item.get("location") or "Remote",
                "url": item.get("url") or f"https://remoteok.com/l/{item['id']}",
                "source": "RemoteOK",
            })
    return jobs


def fetch_arbeitnow(keywords):
    """https://arbeitnow.com/api/job-board-api - public, no auth."""
    jobs = []
    try:
        data = _get_json("https://arbeitnow.com/api/job-board-api")
    except requests.RequestException as e:
        print(f"[arbeitnow] fetch failed: {e}")
        return jobs

    for item in data.get("data", []):
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        if not keywords or any(k.lower() in text for k in keywords):
            jobs.append({
                "id": f"arbeitnow_{item.get('slug', item.get('title'))}",
                "title": item.get("title", "Unknown"),
                "company": item.get("company_name", "Unknown"),
                "location": ", ".join(item.get("location", "").split(",")) or "Remote",
                "url": item.get("url", ""),
                "source": "Arbeitnow",
            })
    return jobs


def fetch_greenhouse(company_slug, keywords):
    """https://boards-api.greenhouse.io/v1/boards/{slug}/jobs - public per-company."""
    jobs = []
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    try:
        data = _get_json(url, params={"content": "true"})
    except requests.RequestException as e:
        print(f"[greenhouse:{company_slug}] fetch failed: {e}")
        return jobs

    for item in data.get("jobs", []):
        text = f"{item.get('title', '')} {item.get('content', '')}".lower()
        if not keywords or any(k.lower() in text for k in keywords):
            jobs.append({
                "id": f"greenhouse_{company_slug}_{item['id']}",
                "title": item.get("title", "Unknown"),
                "company": company_slug,
                "location": (item.get("location") or {}).get("name", "Unknown"),
                "url": item.get("absolute_url", ""),
                "source": "Greenhouse",
            })
    return jobs


def fetch_lever(company_slug, keywords):
    """https://api.lever.co/v0/postings/{slug}?mode=json - public per-company."""
    jobs = []
    url = f"https://api.lever.co/v0/postings/{company_slug}"
    try:
        data = _get_json(url, params={"mode": "json"})
    except requests.RequestException as e:
        print(f"[lever:{company_slug}] fetch failed: {e}")
        return jobs

    for item in data:
        text = f"{item.get('text', '')} {item.get('descriptionPlain', '')}".lower()
        if not keywords or any(k.lower() in text for k in keywords):
            jobs.append({
                "id": f"lever_{company_slug}_{item.get('id')}",
                "title": item.get("text", "Unknown"),
                "company": company_slug,
                "location": (item.get("categories") or {}).get("location", "Unknown"),
                "url": item.get("hostedUrl", ""),
                "source": "Lever",
            })
    return jobs


def fetch_all(keywords, greenhouse_companies=None, lever_companies=None):
    jobs = []
    jobs += fetch_remoteok(keywords)
    jobs += fetch_arbeitnow(keywords)
    for slug in (greenhouse_companies or []):
        jobs += fetch_greenhouse(slug, keywords)
    for slug in (lever_companies or []):
        jobs += fetch_lever(slug, keywords)
    return jobs
