#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

if [ `id -u` -ne 0 ]; then
    echo "Please run this script with sudo"
    exit 1
fi

if [[ -e ../.IPs_env ]]; then
    :
else
    echo -e "\nYou need to configure the 'EXAREME_IP' variable. It is the IP where Exareme master is currently running."
    ../config/check_env_variabe_IP.sh ../.IPs_env EXAREME_IP

    echo -e "\nYou need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from."
    ../config/check_env_variabe_IP.sh ../.IPs_env PUBLIC_MIP_IP

fi
cat ../.IPs_env >> .env ; echo "" >> .env ; cat ../.versions_env >> .env

echo -e "\nRemoving previous services..."

docker-compose --project-name mip_federation down
docker_compose_down=$?
if [[ ${docker_compose_down} -ne 0 ]]; then
    echo -e "\nAn error has occurred while removing services and networks.Exiting.." >&2
    exit 1
else
    :
fi

rm .env