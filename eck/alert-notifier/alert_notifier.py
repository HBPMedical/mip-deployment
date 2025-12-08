"""Alert notifier that posts Elasticsearch/Kibana alert deltas to Teams/Webex."""

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests

from teams_send import send_teams_message
STATE_FILE_ENV = "ALERT_STATE_FILE"
ES_URL_ENV = "ES_URL"
ES_USER_ENV = "ES_USER"
ES_PASS_ENV = "ES_PASS"
ES_INDEX_ENV = "ES_INDEX"
ES_QUERY_SIZE_ENV = "ES_QUERY_SIZE"
ES_SKIP_VERIFY_ENV = "ES_SKIP_VERIFY"
TEAMS_ENABLED_ENV = "ENABLE_TEAMS"
WEBEX_ENABLED_ENV = "ENABLE_WEBEX"
WEBEX_TOKEN_ENV = "WEBEX_BOT_TOKEN"
WEBEX_ROOM_ENV = "WEBEX_ROOM_ID"
WEBEX_EMAIL_ENV = "WEBEX_PERSON_EMAIL"
DEFAULT_STATE_FILENAME = ".alert_notifier_state.json"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_STATE_PATH = SCRIPT_DIR / DEFAULT_STATE_FILENAME
DEFAULT_ES_INDEX = ".internal.alerts-observability.logs.alerts-default-*"
DEFAULT_ES_QUERY_SIZE = 200
COMPARATOR_SYMBOLS = {
    "more than": ">",
    "more than or equals": ">=",
    "less than": "<",
    "less than or equals": "<=",
    "equals": "=",
    "not equals": "!=",
}


def send_webex_message(
    message: str,
    token: Optional[str] = None,
    room_id: Optional[str] = None,
    email: Optional[str] = None,
) -> None:
    """Send a message to Webex via the messages API."""

    resolved_token = token or os.getenv(WEBEX_TOKEN_ENV)
    if not resolved_token:
        raise ValueError("No Webex bot token provided (set WEBEX_BOT_TOKEN or pass --webex-token).")

    resolved_room = room_id or os.getenv(WEBEX_ROOM_ENV)
    resolved_email = email or os.getenv(WEBEX_EMAIL_ENV)

    if not (resolved_room or resolved_email):
        raise ValueError("Provide a Webex room ID or person email via CLI or environment variables.")

    payload: Dict[str, str] = {"text": message}
    if resolved_room:
        payload["roomId"] = resolved_room
    if resolved_email:
        payload["toPersonEmail"] = resolved_email

    response = requests.post(
        "https://webexapis.com/v1/messages",
        headers={
            "Authorization": f"Bearer {resolved_token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"Failed to post alert update to Webex (status {response.status_code}): {response.text}"
        )


def load_alert_payload(path: Path) -> List[Any]:
    """Load current alerts from a JSON file and normalise them to a list."""

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    return _normalise_alert_structure(data)


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _default_es_query(size: int) -> Dict[str, Any]:
    return {
        "size": max(size, 1),
        "query": {
            "bool": {
                "filter": [
                    {"term": {"kibana.alert.status": {"value": "active"}}},
                    {"terms": {"kibana.alert.workflow_status": ["open", "acknowledged"]}},
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}],
    }


def fetch_alerts_from_es(
    es_url: str,
    index: str,
    es_user: Optional[str],
    es_pass: Optional[str],
    size: int,
    verify_ssl: bool,
    query: Optional[Dict[str, Any]] = None,
) -> List[Any]:
    """Pull active alerts from Elasticsearch and normalise the response."""

    if not es_url:
        raise ValueError("ES URL not provided. Set ES_URL or pass --es-url.")

    endpoint = f"{es_url.rstrip('/')}/{index.strip('/')}/_search"
    payload = query or _default_es_query(size)
    auth = (es_user, es_pass) if es_user or es_pass else None

    response = requests.post(
        endpoint,
        headers={"Content-Type": "application/json"},
        json=payload,
        auth=auth,
        timeout=30,
        verify=verify_ssl,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"Failed to fetch alerts from Elasticsearch (status {response.status_code}): {response.text}"
        )

    data = response.json()
    return _normalise_alert_structure(data)


def _normalise_alert_structure(data: Any) -> List[Any]:
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        alerts = data.get("alerts")
        if isinstance(alerts, list):
            return alerts
        hits = data.get("hits")
        if isinstance(hits, dict) and isinstance(hits.get("hits"), list):
            extracted: List[Any] = []
            for hit in hits["hits"]:
                if isinstance(hit, dict) and "_source" in hit:
                    extracted.append(hit["_source"])
                else:
                    extracted.append(hit)
            return extracted
        return [data]
    return [data]


def _load_previous_alerts(state_path: Path) -> List[Any]:
    if not state_path.exists():
        return []
    with state_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return _normalise_alert_structure(data)


def _save_alert_state(state_path: Path, alerts: Sequence[Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(list(alerts), handle, indent=2, sort_keys=True)


def _canonicalise(alert: Any) -> str:
    if isinstance(alert, str):
        return alert.strip()
    try:
        return json.dumps(alert, sort_keys=True)
    except TypeError:
        return str(alert)


def _build_alert_index(alerts: Iterable[Any]) -> Tuple[Counter, Dict[str, Any]]:
    counter: Counter = Counter()
    representatives: Dict[str, Any] = {}
    for alert in alerts:
        key = _canonicalise(alert)
        counter[key] += 1
        representatives.setdefault(key, alert)
    return counter, representatives


def _diff_alerts(old_alerts: Sequence[Any], new_alerts: Sequence[Any]) -> Tuple[List[Tuple[Any, int]], List[Tuple[Any, int]]]:
    """Return (added, resolved) alerts, each as (alert, count) tuples."""

    old_counter, old_map = _build_alert_index(old_alerts)
    new_counter, new_map = _build_alert_index(new_alerts)

    added_counter = new_counter - old_counter
    resolved_counter = old_counter - new_counter

    added = [(new_map[key], count) for key, count in added_counter.items()]
    resolved = [(old_map[key], count) for key, count in resolved_counter.items()]
    return added, resolved


def _format_alert(alert: Any, count: int) -> str:
    if isinstance(alert, str):
        base = alert.strip()
        if count > 1:
            base = f"{base} (x{count})"
    elif isinstance(alert, dict):
        title = (
            alert.get("kibana.alert.rule.name")
            or alert.get("name")
            or alert.get("rule_name")
            or alert.get("rule")
        )
        severity = alert.get("kibana.alert.severity") or alert.get("severity")
        status = alert.get("kibana.alert.status")
        reason = (
            alert.get("kibana.alert.reason")
            or alert.get("reason")
            or alert.get("message")
        )
        context = alert.get("kibana.alert.context") or {}
        conditions = context.get("conditions")
        matching = context.get("matchingDocuments")
        value = alert.get("kibana.alert.evaluation.value")
        threshold = alert.get("kibana.alert.evaluation.threshold")
        comparator = None
        rule_params = alert.get("kibana.alert.rule.parameters") or {}
        count_params = rule_params.get("count") or {}
        comparator = count_params.get("comparator")
        instance = alert.get("kibana.alert.instance.id") or alert.get("instance")
        started = alert.get("kibana.alert.start") or alert.get("start")

        header_parts: List[str] = []
        if title:
            header_parts.append(str(title))
        if severity:
            header_parts.append(str(severity).upper())
        if status:
            header_parts.append(str(status).upper())
        if instance and instance != "*":
            header_parts.append(f"instance={instance}")

        header = " | ".join(header_parts) if header_parts else "Alert"
        if count > 1:
            header += f" (x{count})"

        detail_lines: List[str] = []
        if reason:
            detail_lines.append(f"Reason: {reason}")
        if conditions:
            detail_lines.append(f"Conditions: {conditions}")
        if matching is not None:
            detail_lines.append(f"Matches: {matching}")
        elif value is not None:
            detail_lines.append(f"Value: {value}")
        if threshold is not None:
            comparator_text = COMPARATOR_SYMBOLS.get(str(comparator or "").lower(), comparator)
            if comparator_text:
                detail_lines.append(f"Threshold: {comparator_text} {threshold}")
            else:
                detail_lines.append(f"Threshold: {threshold}")
        if started:
            detail_lines.append(f"Since: {started}")

        if detail_lines:
            base = "\n".join([header] + [f"  - {line}" for line in detail_lines])
        else:
            base = header
    else:
        base = str(alert)
        if count > 1:
            base = f"{base} (x{count})"

    return base


def _format_diff_message(added: List[Tuple[Any, int]], resolved: List[Tuple[Any, int]], total_count: int) -> str:
    lines: List[str] = []
    lines.append("Alert state changed")
    lines.append(f"Current active alerts: {total_count}")

    if added:
        lines.append("New alerts:")
        for alert, count in added:
            lines.append(f"- {_format_alert(alert, count)}")

    if resolved:
        lines.append("Resolved alerts:")
        for alert, count in resolved:
            lines.append(f"- {_format_alert(alert, count)}")

    if not added and not resolved:
        lines.append("No changes detected.")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send alert state changes to Teams and/or Webex.")
    parser.add_argument(
        "alerts",
        nargs="?",
        type=Path,
        help="Path to a JSON file containing the current alerts (list or object). If omitted, alerts are pulled from Elasticsearch.",
    )
    parser.add_argument(
        "--state",
        type=Path,
        default=Path(os.getenv(STATE_FILE_ENV, str(DEFAULT_STATE_PATH))),
        help="Path to the state file that tracks previously sent alerts (default: %(default)s).",
    )
    parser.add_argument(
        "--es-url",
        default=os.getenv(ES_URL_ENV),
        help="Elasticsearch base URL (e.g. https://elastic.example:9200). Defaults to ES_URL env.",
    )
    parser.add_argument(
        "--es-user",
        default=os.getenv(ES_USER_ENV),
        help="Username for Elasticsearch basic auth. Defaults to ES_USER env.",
    )
    parser.add_argument(
        "--es-pass",
        default=os.getenv(ES_PASS_ENV),
        help="Password for Elasticsearch basic auth. Defaults to ES_PASS env.",
    )
    parser.add_argument(
        "--es-index",
        default=os.getenv(ES_INDEX_ENV, DEFAULT_ES_INDEX),
        help="Index pattern to query for alerts. Defaults to %(default)s or ES_INDEX env.",
    )
    parser.add_argument(
        "--es-query-size",
        type=int,
        default=int(os.getenv(ES_QUERY_SIZE_ENV, DEFAULT_ES_QUERY_SIZE)),
        help="Maximum number of alerts to retrieve (default: %(default)s, overridable via ES_QUERY_SIZE env).",
    )
    parser.add_argument(
        "--es-query-file",
        type=Path,
        help="Optional path to a JSON file containing a custom Elasticsearch _search body.",
    )
    parser.add_argument(
        "--es-skip-verify",
        action="store_true",
        default=_env_flag(ES_SKIP_VERIFY_ENV, False),
        help="Disable TLS verification when talking to Elasticsearch (or set ES_SKIP_VERIFY=true).",
    )
    parser.add_argument(
        "--webhook",
        default=os.getenv("TEAMS_WEBHOOK_URL"),
        help="Override Teams webhook URL. Falls back to TEAMS_WEBHOOK_URL or the hard-coded default.",
    )
    teams_toggle = parser.add_mutually_exclusive_group()
    teams_toggle.add_argument(
        "--enable-teams",
        dest="enable_teams",
        action="store_true",
        help="Send notifications to Microsoft Teams (default).",
    )
    teams_toggle.add_argument(
        "--disable-teams",
        dest="enable_teams",
        action="store_false",
        help="Skip Microsoft Teams notifications.",
    )
    webex_toggle = parser.add_mutually_exclusive_group()
    webex_toggle.add_argument(
        "--enable-webex",
        dest="enable_webex",
        action="store_true",
        help="Send notifications to Webex.",
    )
    webex_toggle.add_argument(
        "--disable-webex",
        dest="enable_webex",
        action="store_false",
        help="Skip Webex notifications (default).",
    )
    parser.add_argument(
        "--webex-token",
        default=os.getenv(WEBEX_TOKEN_ENV),
        help="Webex bot token. Defaults to WEBEX_BOT_TOKEN env.",
    )
    parser.add_argument(
        "--webex-room-id",
        default=os.getenv(WEBEX_ROOM_ENV),
        help="Webex roomId to post into (defaults to WEBEX_ROOM_ID env).",
    )
    parser.add_argument(
        "--webex-email",
        default=os.getenv(WEBEX_EMAIL_ENV),
        help="Recipient email for direct messages (defaults to WEBEX_PERSON_EMAIL env).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute differences without sending any notifications.",
    )

    parser.set_defaults(enable_teams=None, enable_webex=None)

    args = parser.parse_args()
    if args.enable_teams is None:
        args.enable_teams = _env_flag(TEAMS_ENABLED_ENV, True)
    if args.enable_webex is None:
        args.enable_webex = _env_flag(WEBEX_ENABLED_ENV, False)

    es_query = None
    if args.es_query_file:
        with args.es_query_file.open("r", encoding="utf-8") as handle:
            es_query = json.load(handle)

    if args.alerts:
        current_alerts = load_alert_payload(args.alerts)
    else:
        verify_ssl = not args.es_skip_verify
        if not args.es_url:
            raise SystemExit("Missing alerts source. Provide a JSON file path or set --es-url / ES_URL.")
        current_alerts = fetch_alerts_from_es(
            es_url=args.es_url,
            index=args.es_index,
            es_user=args.es_user,
            es_pass=args.es_pass,
            size=args.es_query_size,
            verify_ssl=verify_ssl,
            query=es_query,
        )
    previous_alerts = _load_previous_alerts(args.state)

    added, resolved = _diff_alerts(previous_alerts, current_alerts)

    if not added and not resolved:
        print("No alert changes detected; skipping Teams notification.")
        if not args.dry_run:
            _save_alert_state(args.state, current_alerts)
        return

    message = _format_diff_message(added, resolved, len(current_alerts))

    print(message)
    if args.dry_run:
        return

    if args.enable_teams:
        send_teams_message(message, webhook_url=args.webhook)

    if args.enable_webex:
        send_webex_message(
            message,
            token=args.webex_token,
            room_id=args.webex_room_id,
            email=args.webex_email,
        )

    _save_alert_state(args.state, current_alerts)


if __name__ == "__main__":
    main()
