#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

set -o pipefail # trace ERR through pipes
set -o errtrace # trace ERR through 'time command' and other functions

if [[ -e ./.env ]]; then
    :
else
    echo "You need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from. If you only want to install it on your local machine, you can initialize it with 127.0.0.1"
    ./config/check_env_variabe_IP.sh ./.env PUBLIC_MIP_IP
fi

cat ./.env >> ./.env_file ; echo "" >> ./.env_file ; cat ./.versions_env >> ./.env_file

echo -e "\nRemoving previous services..."
docker-compose --project-name mip --env-file ./.env_file down