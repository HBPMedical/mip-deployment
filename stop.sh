#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

if [ `id -u` -ne 0 ]; then
    echo "Please run this script with sudo"
    exit 1
fi

set -o pipefail # trace ERR through pipes
set -o errtrace # trace ERR through 'time command' and other functions

if [[ -e ./.IPs_env ]]; then
    :
else
    echo "You need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from. If you only want to install it on your local machine, you can initialize it with 127.0.0.1"
    ./config/check_env_variabe_IP.sh ./.env PUBLIC_MIP_IP
fi

cat ./.IPs_env >> .env ; echo "" >> .env ; cat ./.versions_env >> .env

echo -e "\nRemoving previous services..."
docker-compose --project-name mip down

rm .env