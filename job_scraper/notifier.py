import platform
import smtplib
import subprocess
from email.mime.text import MIMEText

import config


def send_imessage(body):
    """Sends via AppleScript to Messages.app. Only works when this script
    runs on a Mac with Messages.app signed into an Apple ID/iMessage."""
    if platform.system() != "Darwin":
        print("[notifier] NOTIFY_METHOD=imessage but this isn't a Mac — skipping.")
        print(f"[notifier] Would have sent:\n{body}")
        return
    if not config.IMESSAGE_TO:
        print("[notifier] IMESSAGE_TO not set — skipping.")
        print(f"[notifier] Would have sent:\n{body}")
        return

    # Escape backslashes/quotes so the message text can't break out of the
    # AppleScript string literal.
    escaped_body = body.replace("\\", "\\\\").replace('"', '\\"')
    escaped_to = config.IMESSAGE_TO.replace("\\", "\\\\").replace('"', '\\"')

    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{escaped_to}" of targetService
        send "{escaped_body}" to targetBuddy
    end tell
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[notifier] iMessage send failed: {result.stderr.strip()}")
        print(f"[notifier] Would have sent:\n{body}")


def send_email_sms(body):
    """Sends via Gmail SMTP to a carrier email-to-SMS gateway address —
    free fallback that works from any machine, not just a Mac."""
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


def send_sms(body):
    if config.NOTIFY_METHOD == "imessage":
        send_imessage(body)
    else:
        send_email_sms(body)


def notify_new_jobs(jobs):
    """Batch into one message per run and cap how many postings get spelled
    out so it stays short (matters most for the email-to-SMS fallback,
    which carriers truncate/split)."""
    if not jobs:
        return

    max_listed = 5
    lines = [f"{len(jobs)} new job(s) matching your search:"]
    for job in jobs[:max_listed]:
        lines.append(f"- {job['title']} @ {job['company']} ({job['source']}): {job['url']}")
    if len(jobs) > max_listed:
        lines.append(f"...and {len(jobs) - max_listed} more.")

    send_sms("\n".join(lines))
