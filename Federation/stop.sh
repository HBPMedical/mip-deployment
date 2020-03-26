#!/usr/bin/env bash

echo "" >> ../.versions_env ; cat ../.env >> ../.versions_env

echo -e "\nRemoving previous services..."
docker-compose --project-name mip_federation --env-file ../.versions_env down
docker_compose_down=$?
if [[ ${docker_compose_down} -ne 0 ]]; then
    echo -e "\nAn error has occurred while removing services and networks.Exiting.." >&2
    exit 1
else
    :
fi

sed -i "/EXAREME_IP/d" ../.versions_env
sed -i "/PUBLIC_MIP_IP/d" ../.versions_env