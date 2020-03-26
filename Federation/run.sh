#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

# Checking the EXAREME_IP env variable
echo -e "\nYou need to configure the 'EXAREME_IP' variable. It is the IP where Exareme master is currently running."
../config/check_env_variabe_IP.sh ../.env EXAREME_IP

# Checking the PUBLIC_MIP_IP env variable
echo -e "\nYou need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from."
../config/check_env_variabe_IP.sh ../.env PUBLIC_MIP_IP

echo "" >> ../.versions_env ; cat ../.env >> ../.versions_env

# Creating logs folder
if [ ! -d "logs" ]; then
        mkdir logs
fi
chmod a+rwx logs

echo -e "\nRemoving previous services..."
docker-compose --project-name mip_federation --env-file ../.versions_env down
docker_compose_down=$?
if [[ ${docker_compose_down} -ne 0 ]]; then
    echo -e "\nAn error has occurred while removing services and networks.Exiting.." >&2
    exit 1
else
    :
fi

echo -e "\nDeploy Services..."

docker-compose --project-name mip_federation --env-file ../.versions_env up -d
docker_compose_up=$?
if [[ ${docker_compose_up} -ne 0 ]]; then
    echo -e "\nAn error has occurred while deploying services.Exiting.." >&2
    exit 1
else
    :
fi

echo -e "\nMIP is up and running you can access it on: http://${PUBLIC_MIP_IP}"

sed -i "/EXAREME_IP/d" ../.versions_env
sed -i "PUBLIC_MIP_IP/d" ../.versions_env