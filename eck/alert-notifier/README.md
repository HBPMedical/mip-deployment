# Alert Notifier

This utility polls Kibana alerts and posts state changes to Microsoft Teams and/or Webex. It can run locally for experimentation or inside Kubernetes (via the Helm charts in this repository).

## Local development

1. Set up a virtual environment and install dependencies:
   ```bash
   cd alert-notifier
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Provide credentials and execute the notifier:
   ```bash
   export ES_URL=https://elastic.example:9200
   export ES_USER=elastic
   export ES_PASS=supersecret
   export TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/..."        # optional
   export WEBEX_BOT_TOKEN="<bot-token>"                                     # optional
   export WEBEX_ROOM_ID="Y2lzY29zcGFyazovL3VzL1JPT00v..."                  # or WEBEX_PERSON_EMAIL=user@example.com

   python alert_notifier.py --state /var/lib/alert-notifier/state.json \
     --enable-teams --enable-webex
   ```

   Drop `--enable-teams`/`--enable-webex` (or set the matching `ENABLE_*` env vars) if you only want one destination. Append `--dry-run` to preview the diff without sending messages.

The script accepts either a JSON file containing current alerts or, if no file path is provided, it will query Elasticsearch directly using the credentials above.

### Helper utilities

- `teams_send.py` – send a test message to the configured Teams webhook.
- `webex_send.py` – send a test message to a Webex room or direct recipient. The helper understands `webexteams://` links or UI “space IDs” and converts them to the API `roomId` automatically. Pass `--token` or set `WEBEX_BOT_TOKEN` to supply the bot credential.
- `notifier.py` – one-off Teams poke that reads the webhook from `TEAMS_WEBHOOK_URL`. Use it for quick smoke tests without touching the full notifier.

## Kubernetes integration

The Helm chart under `../kubernetes/` deploys the notifier CronJob alongside Elasticsearch/Kibana/Beats. Provide image details and toggle the outputs via values:

```yaml
# alert-notifier-values.yaml
alertNotifier:
  image:
    repository: registry.example.com/alert-notifier
    tag: latest
  schedule: "*/5 * * * *"
  es:
    index: ".internal.alerts-observability.logs.alerts-default-*"
    skipVerify: true
  teams:
    enabled: true
  webex:
    enabled: true
    roomId: ""          # leave empty to pull from the secret
    personEmail: ""
    tokenKey: webexBotToken
    roomIdKey: webexRoomId
  secret:
    create: false
    existingSecret: alert-notifier-secrets

kibana:
  ingress:
    enabled: true
    hosts:
      - host: localhost
        path: /
        pathType: Prefix
  http:
    tls:
      selfSignedCertificate:
        disabled: true
  config:
    xpack.security.secureCookies: false
```

Deploy (or upgrade) the chart from the repository root:

```bash
helm upgrade --install eck <chart-dir> -f alert-notifier-values.yaml \
  --namespace elastic-system --create-namespace
```

`<chart-dir>` is `kubernetes` or `kubernetes_on_rke2` depending on the defaults you want.

### Secret

Create (or update) the notifier secret before installing the chart. The example below uses the keys expected by the Helm chart:

```bash
kubectl create secret generic alert-notifier-secrets \
  -n elastic-system \
  --from-literal=es-url=https://elasticsearch-sample-es-http.elastic-system.svc:9200 \
  --from-literal=es-user=elastic \
  --from-literal=es-pass="<elastic-password>" \
  --from-literal=teams-webhook="https://outlook.office.com/webhook/..." \
  --from-literal=webexBotToken="<webex-bot-token>" \
  --from-literal=webexRoomId="Y2lzY29zcGFyazovL3VzL1JPT00v..."
```

If you prefer direct messages, omit `webexRoomId` and set `alertNotifier.webex.personEmail` (or `WEBEX_PERSON_EMAIL`).

When the chart provisions a fresh Elasticsearch cluster, retrieve the regenerated `elastic` password and recreate the secret:

```bash
ES_PASS=$(kubectl get secret elasticsearch-sample-es-elastic-user \
  -n elastic-system \
  -o go-template='{{printf "%s" (index .data "elastic")}}' | base64 -d)

kubectl create secret generic alert-notifier-secrets \
  -n elastic-system \
  --from-literal=es-url=https://elasticsearch-sample-es-http.elastic-system.svc:9200 \
  --from-literal=es-user=elastic \
  --from-literal=es-pass="$ES_PASS" \
  --from-literal=teams-webhook="https://outlook.office.com/webhook/..." \
  --from-literal=webexBotToken="<webex-bot-token>" \
  --from-literal=webexRoomId="Y2lzY29zcGFyazovL3VzL1JPT00v..." \
  --dry-run=client -o yaml | kubectl apply -f -
```

### Persistent state

The CronJob stores alert state on a PVC so it only sends deltas. Override `alertNotifier.state.persistence.*` in `values.yaml` to point at an existing claim or disable persistence for ephemeral runs.
