# Beats Deployment


## Kube-state-metrics deployment

Following [this guide](https://last9.io/blog/kube-state-metrics/)

#### Fetch the helm repos:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm repo update
```

#### Install the kube-state-metrics
Metricbeat needs the kube-state-metrics to be running so that it can propagate the system properties to elastic.
```
helm install kube-state-metrics prometheus-community/kube-state-metrics --namespace kube-system
```

## Beats deployment

#### Create an elk user with proper access rights

1. Go to elastic and create a `beats_writer` role with the following:
```
Cluster priviliges:
monitor, manage_index_templates, manage_ilm

Indices:
filebeat-*, metricbeat-*

Priviliges:
write, create, create_index, manage, manage_ilm
```

2. Create a `beats_writer` user with the `beats_writer` role that you created.

3.  Install metricbeat and filebeat after changing the password of the `beats_writer` user in `values.yaml`
```
helm install beats .
```
