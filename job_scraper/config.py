import os

# Search criteria — edit these to match what you're looking for
KEYWORDS = [k.strip() for k in os.environ.get("JOB_KEYWORDS", "account manager").split(",") if k.strip()]
LOCATION = os.environ.get("JOB_LOCATION", "Remote")
REMOTE_ONLY = os.environ.get("JOB_REMOTE_ONLY", "true").lower() == "true"

# Twilio SMS credentials (https://console.twilio.com)
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER", "")
TWILIO_TO_NUMBER = os.environ.get("TWILIO_TO_NUMBER", "")

# Where seen job IDs are persisted so you only get texted about NEW postings
SEEN_JOBS_DB = os.environ.get("SEEN_JOBS_DB", os.path.join(os.path.dirname(__file__), "seen_jobs.json"))

# Companies to check on Greenhouse / Lever (extend this list freely).
# These are ATS platforms companies actually publish stable JSON APIs for.
GREENHOUSE_COMPANIES = [c.strip() for c in os.environ.get("GREENHOUSE_COMPANIES", "").split(",") if c.strip()]
LEVER_COMPANIES = [c.strip() for c in os.environ.get("LEVER_COMPANIES", "").split(",") if c.strip()]
