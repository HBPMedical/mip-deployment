#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

if [ `id -u` -ne 0 ]; then
    echo "Please run this script with sudo"
    exit 1
fi

_valid_IPv4(){
	IP=$1

	if [ "$IP" =~ [^127] ]; then
		return 0
	fi

	if [[ $IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
		for i in 1 2 3 4; do
			if [[ $(echo "${IP}" | cut -d "." -f$i) -gt 255 ]]; then
				return 0
			fi
		done
		return 1
	else
		return 0
	fi
}

_configure_ips(){
	# Checking the IP env variable
	local env_variables_file=$1
	local variable_name=$2

	# If $env_variables_file exists, read the ip
	if [[ -a $env_variables_file ]]; then
		source $env_variables_file
	fi

	if [ -n "${!variable_name}" ]; then
		echo -e "\n'$variable_name' is set to value: ${!variable_name}"
		echo -e "\nWould you like to change it? (y/n)"
		read answer
		while true
		do
			if [[ ${answer} == "y" || ${answer} == "Y" ]]; then
				echo -e "\nRemoving the '$variable_name' from the environment variables file."
				sed -i "/$variable_name/d" $env_variables_file
				break
			elif [[ ${answer} == "n" || ${answer} == "N" ]]; then
				exit 0
			else
				echo "\n'$answer' is not a valid answer! Try again... ( y/n )"
				read answer
			fi
		done
	else
		echo -e "\n'$variable_name' is not set."
	fi


	# Read IP from the user
	echo -e "\nPlease provide a value for the variable '$variable_name': "
	read answer
	_valid_IPv4 $answer
	valid_IP_result=$?
	while [ $valid_IP_result -eq 0 ]; do
		echo -e "\n'$answer' is not a valid IP. Try again... \n"
		read answer
		_valid_IPv4 $answer
		valid_IP_result=$?
	done

	# Store IP to the env file
	echo -e -n "\n$variable_name="${answer} >> $env_variables_file
	# Clean any new lines in file
	sed -i '/^$/d' $env_variables_file
}


# Checking the EXAREME_IP env variable
echo -e "\nYou need to configure the 'EXAREME_IP' variable. It is the IP where Exareme master is currently running."
_configure_ip ../.IPs_env EXAREME_IP

# Checking the PUBLIC_MIP_IP env variable
echo -e "\nYou need to configure the 'PUBLIC_MIP_IP' variable. It is the IP where MIP will be visible from. IP range 127.0.0.0/8 is not allowed at the moment"
_configure_ip ../.IPs_env PUBLIC_MIP_IP

. ../.IPs_env

cat ../.IPs_env >> .env ; echo "" >> .env ; cat ../.versions_env >> .env

# Creating logs folder
if [ ! -d "logs" ]; then
        mkdir logs
fi
chmod a+rwx logs

echo -e "\nRemoving previous services..."
docker-compose --project-name mip_federation down
docker_compose_down=$?
if [[ ${docker_compose_down} -ne 0 ]]; then
    echo -e "\nAn error has occurred while removing services and networks.Exiting.." >&2
    exit 1
else
    :
fi

echo -e "\nDeploy Services..."

docker-compose --project-name mip_federation up -d
docker_compose_up=$?
if [[ ${docker_compose_up} -ne 0 ]]; then
    echo -e "\nAn error has occurred while deploying services.Exiting.." >&2
    rm .env
    exit 1
else
    :
fi

echo -e "\nMIP is up and running you can access it on: http://${PUBLIC_MIP_IP}"

rm .env
