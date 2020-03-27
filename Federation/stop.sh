#!/usr/bin/env bash

cat ../.env >> ./.env_file ; echo "" >> ./.env_file ; cat ../.versions_env >> ./.env_file
return=$?
if [[ ${return} -ne 0 ]]; then
    echo -e "\nMake sure .env file exists.Exiting.." >&2
    exit 1
else
    :
fi

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