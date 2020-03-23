#!/usr/bin/env bash

# Checking the EXAREME_IP env variable
echo -e "\nYou need to configure the 'EXAREME_IP' variable. It is the IP where Exareme master is currently running."
../config/check_env_variabe_IP.sh .env EXAREME_IP

echo -e "\nRemoving previous services..."
docker-compose --project-name mip_federation down

echo -e "\nDeploy Services..."
docker-compose --project-name mip_federation up -d