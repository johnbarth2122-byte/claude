from twilio.rest import Client
import config


def send_sms(body):
    if not all([config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN,
                config.TWILIO_FROM_NUMBER, config.TWILIO_TO_NUMBER]):
        print("[notifier] Twilio not configured — skipping SMS. Set TWILIO_* env vars.")
        print(f"[notifier] Would have sent:\n{body}")
        return

    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    client.messages.create(body=body, from_=config.TWILIO_FROM_NUMBER, to=config.TWILIO_TO_NUMBER)


def notify_new_jobs(jobs):
    """SMS is limited/priced per segment, so batch into one message per run
    and cap how many postings get spelled out to keep it short."""
    if not jobs:
        return

    max_listed = 5
    lines = [f"{len(jobs)} new job(s) matching your search:"]
    for job in jobs[:max_listed]:
        lines.append(f"- {job['title']} @ {job['company']} ({job['source']}): {job['url']}")
    if len(jobs) > max_listed:
        lines.append(f"...and {len(jobs) - max_listed} more.")

    send_sms("\n".join(lines))
