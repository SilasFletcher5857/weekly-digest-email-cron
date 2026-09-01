"""Weekly digest email, scheduled with hosted cron.

cron.create registers a schedule that POSTs to your webhook every Monday; the webhook
builds the digest and calls email.send. Both are one key.
"""
import infrai


def schedule_weekly_digest(webhook_url: str) -> str:
    """Register a Monday-09:00-UTC cron that POSTs to your digest webhook."""
    data = infrai.cron.create(
        name="weekly-digest",
        cron_expr="0 9 * * 1",  # 5-field POSIX; day-of-week is numeric (1 = Monday)
        task=webhook_url,  # cron.create's task is the URL string it fires
    )
    return data["job_id"]


def send_digest(to: str, items: list[str]) -> str:
    """Render the digest and email it (call this from the webhook)."""
    html = "<h1>Your weekly digest</h1><ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
    data = infrai.email.send(to=to, subject="Your weekly digest", html=html)
    return data["message_id"]


if __name__ == "__main__":
    print("scheduled cron:", schedule_weekly_digest("https://app.example.com/hooks/digest"))
    print("sample send:", send_digest("chenhua@changba.com", ["New: dark mode", "Top post of the week"]))
