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

# Optional: specific companies to check via their ATS
export GREENHOUSE_COMPANIES="airbnb,stripe"
export LEVER_COMPANIES="netflix"
```

### Notifications — iMessage (default, requires a Mac)

Only works when this script runs ON a Mac, with Messages.app signed into
your Apple ID/iMessage (there's no cross-platform iMessage API — it works
by driving Messages.app via AppleScript).

```bash
export NOTIFY_METHOD="imessage"
export IMESSAGE_TO="+15551234567"   # or your Apple ID email, exactly as saved in Messages
```

First run may prompt for a macOS permission dialog: allow Terminal (or
whatever runs the script) to control Messages under
**System Settings → Privacy & Security → Automation**.

### Notifications — free SMS fallback (any machine, no Mac needed)

Gmail SMTP → carrier email-to-SMS gateway. Use this if running on a
server/cloud instead of your Mac.

```bash
export NOTIFY_METHOD="email_sms"
# 1. Turn on 2FA on your Google account, then create an App Password:
#    https://myaccount.google.com/apppasswords
# 2. Find your carrier's gateway domain (AT&T: txt.att.net, Verizon: vtext.com,
#    T-Mobile: tmomail.net, Sprint: messaging.sprintpcs.com)
export GMAIL_USER="you@gmail.com"
export GMAIL_APP_PASSWORD="xxxxxxxxxxxxxxxx"   # 16-char app password, not your login password
export SMS_TO_ADDRESS="5551234567@vtext.com"   # your number@carrier gateway
```

## Run

```bash
python main.py
```

Run it on a schedule — it tracks seen job IDs in `seen_jobs.json` so you
only get texted about new postings, not the same ones every run.

Example cron on your Mac (every 30 min) — use `crontab -e`:
```
*/30 * * * * cd /path/to/job_scraper && /usr/bin/python3 main.py >> scraper.log 2>&1
```

Cron on macOS runs with a restricted environment and without the Automation
permission grant tied to your login session, so iMessage sends from cron
often fail silently. If that happens, use a `launchd` agent instead (runs
in your user session, keeps the Automation permission) — ask if you want
one set up.
