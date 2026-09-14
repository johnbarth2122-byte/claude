import smtplib
from email.mime.text import MIMEText

import config


def send_sms(body):
    """Sends via Gmail SMTP to a carrier email-to-SMS gateway address —
    the carrier delivers it to the phone as a real text message, no Twilio
    account or per-message cost required."""
    if not all([config.GMAIL_USER, config.GMAIL_APP_PASSWORD, config.SMS_TO_ADDRESS]):
        print("[notifier] Email-to-SMS not configured — skipping. "
              "Set GMAIL_USER, GMAIL_APP_PASSWORD, SMS_TO_ADDRESS.")
        print(f"[notifier] Would have sent:\n{body}")
        return

    msg = MIMEText(body)
    msg["From"] = config.GMAIL_USER
    msg["To"] = config.SMS_TO_ADDRESS
    msg["Subject"] = ""  # most carrier gateways prepend the subject to the text; keep it empty

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
        server.sendmail(config.GMAIL_USER, [config.SMS_TO_ADDRESS], msg.as_string())


def notify_new_jobs(jobs):
    """Carrier SMS gateways truncate/split long emails, so batch into one
    message per run and cap how many postings get spelled out to keep it short."""
    if not jobs:
        return

    max_listed = 5
    lines = [f"{len(jobs)} new job(s) matching your search:"]
    for job in jobs[:max_listed]:
        lines.append(f"- {job['title']} @ {job['company']} ({job['source']}): {job['url']}")
    if len(jobs) > max_listed:
        lines.append(f"...and {len(jobs) - max_listed} more.")

    send_sms("\n".join(lines))
