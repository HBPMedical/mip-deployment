### ECK


kubectl create -f https://download.elastic.co/downloads/eck/2.12.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.12.0/operator.yaml


#### Enable microk8s hostpath-storage
microk8s enable hostpath-storage

#### Deploy ECK

helm install eck .

#### FIND A WAY TO AVOID PORT-FORWARD

kubectl port-forward -n eck --address localhost,192.168.38.128 service/kibana-kb-http 5601 > port-forward_kibana.log 2>&1 &

kubectl port-forward -n eck --address localhost,192.168.38.128 service/elasticsearch-es-http 9200 > port-forward_elasticsearch.log 2>&1 &

(if deployed)
kubectl port-forward -n eck --address localhost,192.168.38.128 service/logstash-ls-beats 5010 > port-forward_logstash.log 2>&1 &

kubectl get secret -n eck elasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo



#### DEPLOY MIP

# Deploy metric beat FROM KIBANA


GET CA TRUSTED

kubectl get secret -n eck elasticsearch-es-http-certs-public -o jsonpath='{.data.ca\.crt}' | base64 --decode > ca.crt

openssl x509 -fingerprint -sha256 -noout -in ./ca.crt | awk -F '='  '{print $2}' | sed 's/://g'


DEPLOY ELASTIC AGENT

1) GO TO INSTALL METRICBEAT

PREFIX WITH: GIT_EXEC_PATH=/snap/microk8s/current/usr/lib/git-core microk8s 
For example:

GIT_EXEC_PATH=/snap/microk8s/current/usr/lib/git-core microk8s kubectl kustomize https://github.com/elastic/elastic-agent/deploy/kubernetes/elastic-agent-kustomize/default/elastic-agent-standalone\?ref\=v8.17.1 | sed -e 's/JUFQSV9LRVkl/QnVmRzVKUUJWdVR1d1NmQ2ZpUE46akJjdTBCSU5TQXV1bmU3dlJ2SmF5dw==/g' -e "s/%ES_HOST%/https:\/\/192.168.38.128:9200/g" -e "s/%ONBOARDING_ID%/7026907c-8b3a-420d-ae1e-d439d2a494bb/g" -e "s/\(docker.elastic.co\/beats\/elastic-agent:\).*$/\18.17.1/g" -e "s/%CA_TRUSTED%/FECE9C78D825768857EED44CDBBFA5C237F56F514EC4D6203071B326F75551F6/g" | kubectl delete -f-


To delete just change the apply keyword to delete

kubectl kustomize https://github.com/elastic/elastic-agent/deploy/kubernetes/elastic-agent-kustomize/default/elastic-agent-standalone\?ref\=v8.17.1 | sed -e 's/JUFQSV9LRVkl/QnVmRzVKUUJWdVR1d1NmQ2ZpUE46akJjdTBCSU5TQXV1bmU3dlJ2SmF5dw==/g' -e "s/%ES_HOST%/https:\/\/192.168.38.128:9200/g" -e "s/%ONBOARDING_ID%/7026907c-8b3a-420d-ae1e-d439d2a494bb/g" -e "s/\(docker.elastic.co\/beats\/elastic-agent:\).*$/\18.17.1/g" -e "s/%CA_TRUSTED%/FECE9C78D825768857EED44CDBBFA5C237F56F514EC4D6203071B326F75551F6/g" | kubectl delete -f-

