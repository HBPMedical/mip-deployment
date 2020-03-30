#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

if [ `id -u` -ne 0 ]; then
    echo "Please run this script with sudo"
    exit 1
fi

cat ../.versions_env >> .env

echo -e "\nRemoving previous services..."

docker-compose --project-name mip_federation --log-level ERROR down
docker_compose_down=$?
if [[ ${docker_compose_down} -ne 0 ]]; then
    echo -e "\nAn error has occurred while removing services and networks.Exiting.." >&2
    rm .env
    exit 1
else
    :
fi

rm .env