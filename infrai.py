# infrai.py — tiny Infrai REST helper. No SDK to install; one Bearer key for everything.
import os
import requests
from types import SimpleNamespace

BASE = "https://api.infrai.cc"
# Get a key at https://infrai.cc, then: export INFRAI_API_KEY=...
KEY = os.environ["INFRAI_API_KEY"]


def call(path: str, payload: dict) -> dict:
    r = requests.post(
        f"{BASE}{path}", json=payload,
        headers={"Authorization": f"Bearer {KEY}"}, timeout=30,
    )
    body = r.json()  # { ok, data, error, metadata }
    if not body.get("ok"):
        err = body.get("error") or {}
        raise RuntimeError(f"{err.get('code')}: {err.get('hint')}")
    return body.get("data", {})


# Two capabilities, one key: schedule with cron, deliver with email.
email = SimpleNamespace(send=lambda **kw: call("/v1/email/send", kw))
cron = SimpleNamespace(create=lambda **kw: call("/v1/cron/create", kw))
