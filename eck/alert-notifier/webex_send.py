#!/usr/bin/env python3
"""Send a one-off message to Webex using a bot token."""

from __future__ import annotations

import argparse
import base64
import json
import os
from typing import Optional
from urllib.parse import parse_qs, urlparse

import requests


API_URL = "https://webexapis.com/v1/messages"
TOKEN_ENV = "WEBEX_BOT_TOKEN"


def resolve_token(cli_token: Optional[str]) -> str:
    token = (cli_token or os.getenv(TOKEN_ENV) or "").strip()
    if not token:
        raise SystemExit(
            "Provide a Webex bot token via --token or set the WEBEX_BOT_TOKEN environment variable."
        )
    return token


def normalise_room_id(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    raw = raw.strip()
    if raw.startswith("Y2lz"):
        return raw
    if raw.startswith("webexteams://"):
        parsed = urlparse(raw)
        params = parse_qs(parsed.query)
        if "space" in params:
            uuid = params["space"][0]
            return base64.b64encode(f"ciscospark://us/ROOM/{uuid}".encode()).decode()
        if "room" in params:
            return params["room"][0]
    if raw.startswith("http"):
        parsed = urlparse(raw)
        tail = parsed.path.rstrip("/").split("/")[-1]
        try:
            decoded = base64.b64decode(tail).decode()
        except Exception:
            return raw
        if decoded.startswith("https://") and "/conversations/" in decoded:
            uuid = decoded.rsplit("/", 1)[-1]
            return base64.b64encode(f"ciscospark://us/ROOM/{uuid}".encode()).decode()
    return raw


def send_message(token: str, *, room_id: Optional[str], email: Optional[str], text: str) -> dict:
    if not (room_id or email):
        raise ValueError("Provide either --room-id or --email")
    payload: dict[str, str] = {"text": text}
    if room_id:
        payload["roomId"] = room_id
    if email:
        payload["toPersonEmail"] = email

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=15,
    )
    if response.status_code >= 400:
        raise SystemExit(f"Webex API returned {response.status_code}: {response.text}")
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a Webex message using a bot token")
    parser.add_argument("text", nargs="?", default="Test message from our Webex bot")
    parser.add_argument("--room-id", help="roomId or webexteams:// link for the target space")
    parser.add_argument("--email", help="Recipient person email for direct messages")
    parser.add_argument("--token", help="Webex bot token; defaults to WEBEX_BOT_TOKEN env var")
    args = parser.parse_args()

    token = resolve_token(args.token)
    room_id = normalise_room_id(args.room_id)
    result = send_message(token, room_id=room_id, email=args.email, text=args.text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
