"""Tiny helper to fire a Teams webhook from the CLI.
"""

from __future__ import annotations

import os
import sys

import requests

WEBHOOK_ENV = "TEAMS_WEBHOOK_URL"


def get_webhook_url() -> str:
    url = os.getenv(WEBHOOK_ENV, "").strip()
    if not url:
        raise SystemExit(f"Set {WEBHOOK_ENV} before running this helper.")
    return url


def send_teams_message(message: str):
    payload = {"message": message}
    response = requests.post(get_webhook_url(), json=payload, timeout=15)
    print("Status:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    text = "Test message" if len(sys.argv) == 1 else " ".join(sys.argv[1:])
    send_teams_message(text)
