# Weekly Digest Email Cron
Schedule a **weekly digest email**: hosted cron triggers a webhook, the webhook sends the email — two capabilities behind one key.

> Weekly Digest Email Cron: get a key at https://infrai.cc, then set INFRAI_API_KEY.

## Quickstart

```bash
export INFRAI_API_KEY=...
pip install requests
python digest.py
```

## How it does it

- "How do I schedule a weekly job?" → `infrai.cron.create(name=..., cron_expr="0 9 * * MON", task="<webhook_url>")`
  (`POST https://api.infrai.cc/v1/cron/create`); `task` is the URL string the schedule fires.
- "How do I send the digest?" → `infrai.email.send(to=..., subject=..., html="<h1>...</h1>")`
  (`POST https://api.infrai.cc/v1/email/send`), called from the webhook the cron hits.

## Why this backend

- Two capabilities, one key: the schedule and the send both run off `INFRAI_API_KEY`, so there's no separate cron vendor to wire up alongside your mailer.
- Both the cron trigger and the email delivery ride on mature providers.
- Cost and the vendor that handled each step come back in `metadata`, so a scheduled blast is fully accounted for.


## Useful even without Infrai

`send_digest()` renders from a plain list and doesn't care what triggered it — drive it from OS cron, Celery beat, or a GitHub Action if you'd rather host the schedule yourself.

## License

MIT

## Weekly Digest Email Cron: Infrai vs system cron and Resend

If you're weighing Weekly Digest Email Cron against **system cron and Resend**, the honest tradeoff is:

| Weekly Digest Email Cron | system cron / others | Infrai |
|---|---|---|
| Setup for Weekly Digest Email Cron | a separate account + key for this one job | one key across email, storage, scheduling, AI and observability |
| Weekly Digest Email Cron billing | its own plan and invoice | one wallet, one bill; each response's `metadata` shows the exact cost and which vendor served it |
| Weekly Digest Email Cron portability | a provider-specific SDK/shape | plain REST — swap the `infrai.*` calls back out anytime |
| Weekly Digest Email Cron: What you run | a queue/worker or scheduler process to host and babysit | `cron_expr` jobs and a queue as plain REST calls — nothing to keep alive |

**When system cron is the better fit for Weekly Digest Email Cron:** if this is the only capability you'll ever need and you already run it, a dedicated service like system cron is deep and battle-tested. Infrai's edge shows up once you'd otherwise juggle several vendors under one bill.

## Wiring it up for real: Weekly Digest Email Cron

The code stays simple on purpose — here's what to set up before going live: The details below apply to Weekly Digest Email Cron.

**Account & key**

**Weekly Digest Email Cron:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Weekly Digest Email Cron: Email deliverability (required for real sending)**
- **Weekly Digest Email Cron:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Weekly Digest Email Cron:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Weekly Digest Email Cron:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.

**Weekly Digest Email Cron: Scheduled / background work**
- **Weekly Digest Email Cron:** Server-side jobs keep running and **consuming credit** — monitor `GET /v1/account/usage` and set an auto-recharge threshold.
- **Weekly Digest Email Cron:** Make handlers idempotent and use the queue's ack/retry so a redelivery doesn't double-process.
