#!/usr/bin/env bash

# Checking the EXAREME_IP env variable
echo -e "\nYou need to configure the 'EXAREME_IP' variable. It is the IP where Exareme master is currently running."
../config/check_env_variabe_IP.sh .env EXAREME_IP

# Checking the PUBLIC_MIP_IP env variable
echo -e "\nYou need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from. If you only want to install it on your local machine, you can initialize it with 127.0.0.1"
../config/check_env_variabe_IP.sh .env PUBLIC_MIP_IP

. ../.env

echo -e "\nRemoving previous services..."
docker-compose --project-name mip_federation down

echo -e "\nDeploy Services..."

docker-compose --project-name mip_federation up -d
docker_compose_up=$?
if [[ ${docker_compose_up} -ne 0 ]]; then
    echo -e "\nAn error has occurred while deploying services.Exiting.." >&2
    exit 1
else
    :
fi

# Disabling the Keycloak SSL Certificate
echo -e "\nConfiguring Keycloak..."

docker_login_worked=1
count=0
# If status code != 0 an error has occurred
while [[ ${docker_login_worked} -ne 0 ]]
do

	# Wait for keycloak to start
	sleep 20

	# Login to the docker container
	{
		docker exec -it $(docker ps --filter name="mip_federation_keycloak_1" -q) /opt/jboss/keycloak/bin/kcadm.sh config credentials --server http://${PUBLIC_MIP_IP}:8095/auth --realm master --user admin --password Pa55w0rd
	} &> /dev/null
	# Get the status code from previous command
	docker_login_worked=$?

	# Try 10 times and then throw error
	count=`expr $count + 1`
	if [[ ${count} -eq 10 ]]; then
		echo -e "\nCould not configure Keycloak properly. Please try running the script again." >&2
		exit 1
	fi
done

# Disable sslRequired on Keycloak
docker exec -it $(docker ps --filter name="mip_federation_keycloak_1" -q) /opt/jboss/keycloak/bin/kcadm.sh update realms/master -s sslRequired=NONE

echo -e "\nMIP is up and running you can access it on: http://${PUBLIC_MIP_IP}"