# Job Scraper

Pulls new job postings matching your keywords and texts you the new ones.

## Sources
- RemoteOK (public API)
- Arbeitnow (public API)
- Greenhouse (per-company, add slugs to `GREENHOUSE_COMPANIES`)
- Lever (per-company, add slugs to `LEVER_COMPANIES`)

LinkedIn/Indeed are not scraped directly — they block scrapers with login walls
and anti-bot detection, which breaks fast and often. These sources publish
stable public JSON instead.

## Setup

```bash
pip install -r requirements.txt
```

Set env vars (or export in your shell / `.env` + a loader):

```bash
export JOB_KEYWORDS="account manager,client success,customer success"
export JOB_LOCATION="Remote"

# Free SMS via Gmail -> carrier email-to-SMS gateway (no Twilio account needed)
# 1. Turn on 2FA on your Google account, then create an App Password:
#    https://myaccount.google.com/apppasswords
# 2. Find your carrier's gateway domain (AT&T: txt.att.net, Verizon: vtext.com,
#    T-Mobile: tmomail.net, Sprint: messaging.sprintpcs.com)
export GMAIL_USER="you@gmail.com"
export GMAIL_APP_PASSWORD="xxxxxxxxxxxxxxxx"   # 16-char app password, not your login password
export SMS_TO_ADDRESS="5551234567@vtext.com"   # your number@carrier gateway

# Optional: specific companies to check via their ATS
export GREENHOUSE_COMPANIES="airbnb,stripe"
export LEVER_COMPANIES="netflix"
```

## Run

```bash
python main.py
```

Run it on a schedule (cron, GitHub Actions, etc.) — it tracks seen job IDs in
`seen_jobs.json` so you only get texted about new postings, not the same ones
every run.

Example cron (every 30 min):
```
*/30 * * * * cd /path/to/job_scraper && /usr/bin/python3 main.py >> scraper.log 2>&1
```
