import os

# Search criteria — edit these to match what you're looking for
KEYWORDS = [k.strip() for k in os.environ.get("JOB_KEYWORDS", "account manager").split(",") if k.strip()]
LOCATION = os.environ.get("JOB_LOCATION", "Remote")
REMOTE_ONLY = os.environ.get("JOB_REMOTE_ONLY", "true").lower() == "true"

# Free SMS via Gmail SMTP -> carrier email-to-SMS gateway (no Twilio needed).
# GMAIL_USER/GMAIL_APP_PASSWORD: create an App Password at
#   https://myaccount.google.com/apppasswords (requires 2FA enabled on the account)
# SMS_TO_ADDRESS: your_number@carrier_gateway, e.g.:
#   AT&T:      5551234567@txt.att.net
#   Verizon:   5551234567@vtext.com
#   T-Mobile:  5551234567@tmomail.net
#   Sprint:    5551234567@messaging.sprintpcs.com
GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
SMS_TO_ADDRESS = os.environ.get("SMS_TO_ADDRESS", "")

# Where seen job IDs are persisted so you only get texted about NEW postings
SEEN_JOBS_DB = os.environ.get("SEEN_JOBS_DB", os.path.join(os.path.dirname(__file__), "seen_jobs.json"))

# Companies to check on Greenhouse / Lever (extend this list freely).
# These are ATS platforms companies actually publish stable JSON APIs for.
GREENHOUSE_COMPANIES = [c.strip() for c in os.environ.get("GREENHOUSE_COMPANIES", "").split(",") if c.strip()]
LEVER_COMPANIES = [c.strip() for c in os.environ.get("LEVER_COMPANIES", "").split(",") if c.strip()]
