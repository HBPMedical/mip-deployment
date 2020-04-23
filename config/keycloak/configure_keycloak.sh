#!/usr/bin/env bash


# Run the keycloak configuration

echo -e "\nTrying to configure the authorization module."

docker exec -it $(docker ps --filter name="mip_keycloak_1" -q) /opt/jboss/keycloak/bin/kcadm.sh config credentials --server http://keycloak:8095/auth --realm master --user admin --password Pa55w0rd && docker exec -it $(docker ps --filter name="mip_keycloak_1" -q) /opt/jboss/keycloak/bin/kcadm.sh update realms/master -s sslRequired=NONE 

docker_login_worked=$?

if [[ ${docker_login_worked} -ne 0 ]]; then
	echo -e "\nThe authorization module could not be configured. Access to the administration console is unavailable."
else
	echo -e "\nThe authorization module was configured properly."
fi
