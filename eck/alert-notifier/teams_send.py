#!/usr/bin/env python3
"""Send a simple message to Microsoft Teams via incoming webhook."""

from __future__ import annotations

import argparse
import json
import os
from typing import Optional

import requests


DEFAULT_WEBHOOK_URL = ""
TEAMS_WEBHOOK_ENV = "TEAMS_WEBHOOK_URL"


def send_teams_message(message: str, webhook_url: Optional[str] = None) -> None:
    """Send a plain text message to Microsoft Teams via the incoming webhook."""

    resolved_webhook = webhook_url or os.getenv(TEAMS_WEBHOOK_ENV) or DEFAULT_WEBHOOK_URL
    if not resolved_webhook:
        raise ValueError(
            "No Teams webhook URL configured. Set TEAMS_WEBHOOK_URL or pass --webhook."
        )

    payload = {"message": message}
    headers = {"Content-Type": "application/json"}

    response = requests.post(resolved_webhook, headers=headers, data=json.dumps(payload), timeout=30)
    if response.status_code >= 400:
        raise RuntimeError(
            f"Failed to post alert update to Teams (status {response.status_code}): {response.text}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a single message to Microsoft Teams")
    parser.add_argument("text", nargs="?", default="Test message from the Teams helper")
    parser.add_argument("--webhook", help="Teams webhook URL; defaults to TEAMS_WEBHOOK_URL env")
    args = parser.parse_args()

    send_teams_message(args.text, webhook_url=args.webhook)
    print("Message sent to Teams.")


if __name__ == "__main__":
    main()
