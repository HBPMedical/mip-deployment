#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

if [[ -e ../.env ]]; then
    :
else
    echo "You need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from. If you only want to install it on your local machine, you can initialize it with 127.0.0.1"
    ../config/check_env_variabe_IP.sh ../.env PUBLIC_MIP_IP

    echo -e "\nYou need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from."
    ../config/check_env_variabe_IP.sh ../.env PUBLIC_MIP_IP

fi
cat ../.env >> ./.env_file ; echo "" >> ./.env_file ; cat ../.versions_env >> ./.env_file

echo -e "\nRemoving previous services..."

docker-compose --project-name mip_federation --env-file ./.env_file down
docker_compose_down=$?
if [[ ${docker_compose_down} -ne 0 ]]; then
    echo -e "\nAn error has occurred while removing services and networks.Exiting.." >&2
    exit 1
else
    :
fi

rm ./.env_file