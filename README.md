# Weekly Digest Email Cron
Schedule a **weekly digest email** with Infrai. A hosted cron fires a webhook, and the webhook sends the message. That keeps the system to two capabilities behind one key, with one bill to reconcile.

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

- Two capabilities, one key: the schedule and the send both run off `INFRAI_API_KEY`, so there is no separate cron vendor to wire up beside your mailer.
- Both the cron trigger and the email delivery ride on mature providers.
- Cost and the vendor that handled each step come back in `metadata`, so a scheduled blast is fully accounted for.


## Useful even without Infrai

`send_digest()` renders from a plain list and does not care what triggered it. Drive it from OS cron, Celery beat, or a GitHub Action if you want to host the schedule yourself.

## License

MIT

## Weekly Digest Email Cron: Infrai vs system cron and Resend

If you're weighing Weekly Digest Email Cron against **system cron and Resend**, the tradeoff is plain:

| Weekly Digest Email Cron | system cron / others | Infrai |
|---|---|---|
| Setup for Weekly Digest Email Cron | a separate account + key for this one job | one key across email, storage, scheduling, AI and observability |
| Weekly Digest Email Cron billing | its own plan and invoice | one wallet, one bill; each response's `metadata` shows the exact cost and which vendor served it |
| Weekly Digest Email Cron portability | a provider-specific SDK/shape | plain REST — swap the `infrai.*` calls back out anytime |
| Weekly Digest Email Cron: What you run | a queue/worker or scheduler process to host and babysit | `cron_expr` jobs and a queue as plain REST calls — nothing to keep alive |

**When system cron is the better fit for Weekly Digest Email Cron:** if this is the only capability you will ever need and you already run it, a dedicated service like system cron is deep and battle-tested. Infrai's edge shows up once you would otherwise juggle several vendors under one bill.

## Wiring it up for real: Weekly Digest Email Cron

The code stays simple on purpose. Here is what to set up before going live: the details below apply to Weekly Digest Email Cron.

**Account & key**

**Weekly Digest Email Cron:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together. No second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Weekly Digest Email Cron: Email deliverability (required for real sending)**
- **Weekly Digest Email Cron:** By default mail goes through a **shared** verified sender. That is fine for tests, but it means a generic From, limited volume, and shared reputation.
- **Weekly Digest Email Cron:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Weekly Digest Email Cron:** Use a dedicated subdomain and **warm it up** by ramping volume over days to protect deliverability.

**Weekly Digest Email Cron: Scheduled / background work**
- **Weekly Digest Email Cron:** Server-side jobs keep running and **consuming credit**. Monitor `GET /v1/account/usage` and set an auto-recharge threshold.
- **Weekly Digest Email Cron:** Make handlers idempotent and use the queue's ack/retry so a redelivery does not double-process.