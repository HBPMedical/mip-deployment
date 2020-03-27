#!/usr/bin/env bash

set -o pipefail # trace ERR through pipes
set -o errtrace # trace ERR through 'time command' and other functions
set -o errexit  ## set -e : exit the script if any statement returns a non-true return value

cat ./.env >> ./.env_file ; echo "" >> ./.env_file ; cat ./.versions_env >> ./.env_file
return=$?
if [[ ${return} -ne 0 ]]; then
    echo -e "\nMake sure .env file exists.Exiting.." >&2
    exit 1
else
    :
fi

echo -e "\nRemoving previous services..."
docker-compose --project-name mip --env-file ./.env_file down