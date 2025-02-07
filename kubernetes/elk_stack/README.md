# ELK Deployment

## Certificate Creation
Download elasticstack cert utils from [here](https://www.elastic.co/downloads/elasticsearch)

#### Generate Certificate Authority
```
bin/elasticsearch-certutil ca --pem -out elastic-stack-ca.zip
unzip elastic-stack-ca.zip -d certs/
```

#### Generate elasticsearch certificates
```
bin/elasticsearch-certutil cert --name elasticsearch \
 --dns elasticsearch,elasticsearch.default.svc.cluster.local \
 --ca-cert certs/ca.crt \
 --ca-key certs/ca.key \
 --pem -out elastic-cert.zip

unzip elastic-cert.zip -d certs/
```


#### Generate kibana certificates
```
bin/elasticsearch-certutil cert --name kibana \
 --dns kibana,kibana.default.svc.cluster.local \
 --ca-cert certs/ca.crt \
 --ca-key certs/ca.key \
 --pem -out kibana-cert.zip

unzip kibana-cert.zip -d certs/
```

#### Move all the certificates in the proper folders
Replace the default certificates that exist with the ones that you created in the appropriate folders.


### Configure elasticsearch passwords
```
kubectl exec -it -n elk <ELASTICSEARCH-POD> -- bin/elasticsearch-setup-passwords interactive -E http.host=127.0.0.1
```

Kibana should be deployed with the password that you define here. Same for the rest of the beats services.
