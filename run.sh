#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

if [ `id -u` -ne 0 ]; then
    echo "Please run this script with sudo"
    exit 1
fi

set -o pipefail # trace ERR through pipes
set -o errtrace # trace ERR through 'time command' and other functions



# MIP Installation
echo -e "\nStarting the MIP installation."



# Creating logs folder
if [ ! -d "logs" ]; then
        mkdir logs
fi
chmod a+rwx logs



# Running the pathologies.json generator
echo -e "\nDo you want to auto-generate the config files? ( Y/N )"
read answer
while true
do
	if [[ ${answer} == "y" || ${answer} == "Y" ]]; then
		echo -e "\nAuto-generating the config files..."
		./config/pathologies_generator.py -n
		break
	elif [[ ${answer} == "n" || ${answer} == "N" ]]; then
		echo -e "\nYou can change the configurations (pathologies.json) manually from the config folder."
		break
	else
		echo -e "\n$answer is not a valid answer! Try again... ( Y/N )"
		read answer
	fi
done



# CSVs and metadata validation
echo -e "\nValidating if the CSVs match with the metadata..."
rm -rf data/**/*.db	# Removing previous .db files
python config/convert-csv-dataset-to-db.py -f data/ -t "master" # Running the database creation script
py_script=$?
if [[ ${py_script} -ne 0 ]]; then
    echo -e "\nThe CSVs could not be parsed using the metadata. Exiting..." >&2
    exit 1
else
    echo -e "\nThe CSVs match with the metadata."
fi



# Checking the PUBLIC_MIP_IP env variable
echo -e "\nYou need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from. If you only want to install it on your local machine, you can initialize it with 127.0.0.1"
./config/check_env_variabe_IP.sh .IPs_env PUBLIC_MIP_IP

source ./.IPs_env # Load the env variables

cat ./.IPs_env >> .env ; echo "" >> .env ; cat ./.versions_env >> .env

# Removing previous services
echo -e "\nRemoving previous services..."
docker-compose --project-name mip down
docker_compose_down=$?
if [[ ${docker_compose_down} -ne 0 ]]; then
    echo -e "\nAn error has occurred while removing services and networks.Exiting.." >&2
    rm .env
    exit 1
else
    :
fi


# Deploying MIP services
echo -e "\nDeploy Services..."
docker-compose --project-name mip up -d
docker_compose_up=$?
if [[ ${docker_compose_up} -ne 0 ]]; then
    echo -e "\nAn error has occurred while deploying services.Exiting.." >&2
    rm .env
    exit 1
else
    :
fi

# Disabling the Keycloak SSL Certificate
echo -e "\nConfiguring Keycloak..."

docker_login_worked=1
count=0
# If status code != 0 an error has occurred
while [[ ${docker_login_worked} -ne 0 ]]
do
	
	# Wait for keycloak to start
	sleep 20

	# Login to the docker container
	{
		docker exec -it $(docker ps --filter name="mip_keycloak_1" -q) /opt/jboss/keycloak/bin/kcadm.sh config credentials --server http://keycloak:8095/auth --realm master --user admin --password Pa55w0rd
	} &> /dev/null
	# Get the status code from previous command
	docker_login_worked=$?
	
	# Try 5 times and then throw error
	count=`expr $count + 1`
	if [[ ${count} -eq 5 ]]; then
		echo -e "\nMIP is up and running on: http://${PUBLIC_MIP_IP} but  could not be configured properly. \nAs a result you can't access the administration console. You can retry by runnining ./config/configure_keycloak.sh" >&2
		rm .env
		exit 1
	fi
done

# Disable sslRequired on Keycloak
docker exec -it $(docker ps --filter name="mip_keycloak_1" -q) /opt/jboss/keycloak/bin/kcadm.sh update realms/master -s sslRequired=NONE 



echo -e "\nMIP is up and running you can access it on: http://${PUBLIC_MIP_IP}"

rm .env
