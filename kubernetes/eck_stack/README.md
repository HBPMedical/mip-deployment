## ECK


### ECK stack deployment

1. Start the elastic operator
```
kubectl create -f https://download.elastic.co/downloads/eck/2.12.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.12.0/operator.yaml
```

2. Enable microk8s hostpath-storage
```
microk8s enable hostpath-storage
```

3. Deploy ECK

```
helm install eck .
```

4. Get the password of the elastic user
```
kubectl get secret -n eck elasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo
```


### Elastic agents deployment

1. Go to kibana and select `Install Filebeat`

2. Select `kubernetes` deployment

3. Select `Elastic Agent`

4. Store the command for future usage

5. Run the command in the k8s cluster you want to monitor

6. If you want to remove the elastic agents, run the command again replacing the `kubectl apply -f-` with `kubectl delete -f-`

7. (Optional) In some older version of microk8s you could get some git errors when running this command. Try prefixing it with:
```
GIT_EXEC_PATH=/snap/microk8s/current/usr/lib/git-core microk8s 
```

#### (Optional) Elastic agents deployment locally

1. If you want to use the elastic agents internally, not behind a reverse proxy with signed certificates, you need to get the content authority of the certificates:
```
kubectl get secret -n eck elasticsearch-es-http-certs-public -o jsonpath='{.data.ca\.crt}' | base64 --decode > ca.crt

openssl x509 -fingerprint -sha256 -noout -in ./ca.crt | awk -F '='  '{print $2}' | sed 's/://g'
```

2. In the elastic agent command use this env variable:
```
-e "s/%CA_TRUSTED%/FECE9C78D825768857EED44CDBBFA5C237F56F514EC4D6203071B326F75551F6/g"
```

with your own `CA_TRUSTED` value, from the previous command.

The command should look like this:
```
microk8s kubectl kustomize https://github.com/elastic/elastic-agent/deploy/kubernetes/elastic-agent-kustomize/default/elastic-agent-standalone\?ref\=v8.17.1 | sed -e 's/JUFQSV9LRVkl/QnVmRzVKUUJWdVR1d1NmQ2ZpUE46akJjdTBCSU5TQXV1bmU3dlJ2SmF5dw==/g' -e "s/%ES_HOST%/https:\/\/192.168.38.128:9200/g" -e "s/%ONBOARDING_ID%/7026907c-8b3a-420d-ae1e-d439d2a494bb/g" -e "s/\(docker.elastic.co\/beats\/elastic-agent:\).*$/\18.17.1/g" -e "s/%CA_TRUSTED%/FECE9C78D825768857EED44CDBBFA5C237F56F514EC4D6203071B326F75551F6/g" | kubectl delete -f-
```
