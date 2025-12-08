{{- define "eck-stack.fullname" -}}
{{- if .Chart.Name -}}
{{- printf "%s" .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "eck-stack" -}}
{{- end -}}
{{- end -}}

{{- define "eck-stack.alertNotifier.fullname" -}}
{{- printf "%s-alert-notifier" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "eck-stack.alertNotifier.labels" -}}
app.kubernetes.io/name: {{ include "eck-stack.alertNotifier.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | trunc 63 | trimSuffix "-" }}
{{- end -}}

{{- define "eck-stack.alertNotifier.secretName" -}}
{{- $cfg := .Values.alertNotifier.secret | default (dict) -}}
{{- if $cfg.existingSecret -}}
{{- $cfg.existingSecret -}}
{{- else -}}
{{- $name := $cfg.name | default (printf "%s-alert-notifier-secrets" .Release.Name) -}}
{{- $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "eck-stack.alertNotifier.pvcName" -}}
{{- $cfg := .Values.alertNotifier.state.persistence | default (dict) -}}
{{- if $cfg.existingClaim -}}
{{- $cfg.existingClaim -}}
{{- else -}}
{{- printf "%s-alert-notifier-state" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{- define "eck-stack.alertNotifier.image" -}}
{{- $img := .Values.alertNotifier.image | default (dict) -}}
{{- $repo := $img.repository | default "alert-notifier" -}}
{{- $tag := $img.tag | default "latest" -}}
{{- printf "%s:%s" $repo $tag -}}
{{- end -}}

{{- define "eck-stack.alertNotifier.stateFile" -}}
{{- $path := .Values.alertNotifier.state.path | default "/var/lib/alert-notifier/state.json" -}}
{{- if $path -}}
{{- $path -}}
{{- else -}}
/var/lib/alert-notifier/state.json
{{- end -}}
{{- end -}}

{{- define "eck-stack.alertNotifier.stateDir" -}}
{{- $file := include "eck-stack.alertNotifier.stateFile" . -}}
{{- $dir := regexReplaceAll "[^/]+$" $file "" -}}
{{- $trimmed := trimSuffix "/" $dir -}}
{{- if $trimmed -}}
{{- $trimmed -}}
{{- else -}}
/var/lib/alert-notifier
{{- end -}}
{{- end -}}

{{- define "eck-stack.operatorNamespace" -}}
{{- .Values.operator.namespace | default "elastic-system" -}}
{{- end -}}

{{- define "eck-stack.operatorLabels" -}}
app.kubernetes.io/name: {{ include "eck-stack.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: "{{ .Values.operator.version }}"
control-plane: elastic-operator
{{- end -}}

{{- define "eck-stack.operatorSelectorLabels" -}}
control-plane: elastic-operator
{{- end -}}

{{- define "eck-stack.operatorImage" -}}
{{- printf "%s:%s" (.Values.operator.image.repository | default "docker.elastic.co/eck/eck-operator") (.Values.operator.image.tag | default .Values.operator.version) -}}
{{- end -}}

{{- define "eck-stack.operatorConfig" -}}
{{- $config := deepCopy (.Values.operator.config | default (dict)) -}}
{{- $ns := include "eck-stack.operatorNamespace" . -}}
{{- if not $config }}
  {{- $config = dict -}}
{{- end -}}
{{- $currentNs := (index $config "operator-namespace") | default "" -}}
{{- if not $currentNs }}
  {{- $_ := set $config "operator-namespace" $ns -}}
{{- end -}}
{{- if .Values.operator.webhook.enabled }}
  {{- $_ := set $config "enable-webhook" true -}}
  {{- $_ := set $config "webhook-port" (.Values.operator.webhook.port | default 9443) -}}
{{- else }}
  {{- $_ := set $config "enable-webhook" false -}}
{{- end -}}
{{- toYaml $config -}}
{{- end -}}
