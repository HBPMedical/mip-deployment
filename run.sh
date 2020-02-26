#!/usr/bin/env bash

if [ `id -u` -ne 0 ]; then
    echo "Please run this script with sudo"
    exit 1
fi

set -o pipefail # trace ERR through pipes
set -o errtrace # trace ERR through 'time command' and other functions
set -o errexit  ## set -e : exit the script if any statement returns a non-true return value

if [ ! -d "logs" ]; then
        mkdir logs
fi

chmod a+rwx logs

echo -e "\nRemoving previous services..."
docker-compose --project-name mip down

echo -e "\nDeploy Services..."
docker-compose --project-name mip up -d
