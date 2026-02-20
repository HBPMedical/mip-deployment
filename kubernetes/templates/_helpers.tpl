{{- define "mip.namespace" -}}
{{- default "default" .Values.cluster.namespace -}}
{{- end -}}

{{- define "mip.instanceName" -}}
{{- printf "%s %s" (default "MIP" .Values.mip.displayName) (default "latest" .Values.mip.version) -}}
{{- end -}}

{{- define "mip.instanceVersion" -}}
{{- $frontend := default "" .Values.frontend.image.tag -}}
{{- $backend := default "" .Values.portalbackend.image.tag -}}
{{- $exareme := default "" .Values.engines.exaflow.image.tag -}}
{{- printf "Frontend: %s, Backend: %s, Exareme: %s" $frontend $backend $exareme -}}
{{- end -}}

{{- define "mip.keycloak.enabled" -}}
{{- ternary true false (default true .Values.keycloak.enabled) -}}
{{- end -}}

{{- define "mip.keycloak.protocol" -}}
{{- default "https" .Values.keycloak.protocol -}}
{{- end -}}

{{- define "mip.keycloak.host" -}}
{{- default "" .Values.keycloak.host -}}
{{- end -}}

{{- define "mip.keycloak.realm" -}}
{{- default "MIP" .Values.keycloak.realm -}}
{{- end -}}

{{- define "mip.keycloak.clientId" -}}
{{- default "" .Values.keycloak.clientId -}}
{{- end -}}

{{- define "mip.keycloak.sslRequired" -}}
{{- default "external" .Values.keycloak.sslRequired -}}
{{- end -}}

{{- define "mip.keycloak.authUrl" -}}
{{- $protocol := include "mip.keycloak.protocol" . -}}
{{- $host := include "mip.keycloak.host" . -}}
{{- if and $protocol $host -}}
{{- printf "%s://%s/auth/" $protocol $host -}}
{{- else -}}
{{- "" -}}
{{- end -}}
{{- end -}}
