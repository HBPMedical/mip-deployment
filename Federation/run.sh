#!/usr/bin/env bash

# Checking the EXAREME_IP env variable
echo -e "\nYou need to configure the 'EXAREME_IP' variable. It is the IP where Exareme master is currently running."
../config/check_env_variabe_IP.sh .env EXAREME_IP

# Checking the PUBLIC_MIP_IP env variable
echo -e "\nYou need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from. If you only want to install it on your local machine, you can initialize it with 127.0.0.1"
./config/check_env_variabe_IP.sh .env PUBLIC_MIP_IP

echo -e "\nRemoving previous services..."
docker-compose --project-name mip_federation down

echo -e "\nDeploy Services..."
docker-compose --project-name mip_federation up -d