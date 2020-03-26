#!/usr/bin/env bash


valid_IP () {
    IP=$1
	
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


env_variables_file=$1
variable_name=$2

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
valid_IP $answer
valid_IP_result=$?
while [ $valid_IP_result -eq 0 ]
do
	echo -e "\n'$answer' is not a valid IP. Try again... \n"
	read answer
	valid_IP $answer
	valid_IP_result=$?
done

# Store IP to the env file
echo -e -n "\n$variable_name="${answer} >> $env_variables_file
# Clean any new lines in file
 sed -i '/^$/d' $env_variables_file
