#!/usr/bin/env bash

if [ `id -u` -ne 0 ]; then
    echo "Please run this script with sudo"
    exit 1
fi

set -o pipefail # trace ERR through pipes
set -o errtrace # trace ERR through 'time command' and other functions

if [ ! -d "logs" ]; then
        mkdir logs
fi

chmod a+rwx logs

echo "Starting the process of creating databases..Deleting previous ones.."
chmod 775 convert-csv-dataset-to-db.py
#Removing all previous .db files from the data/
rm -rf data/**/*.db

echo -e "\nParsing CSV files from data/ to Database files. "
python convert-csv-dataset-to-db.py -f data/ -t "master" 2> /dev/null
#Get the status code from previous command
py_script=$?
#If status code != 0 an error has occurred
if [[ ${py_script} -ne 0 ]]; then
     echo -e "\nCreation of databases failed. Exiting.." >&2
     exit 1
else
    echo -e "\nDatabase files created."
fi

echo -e "\nRemoving previous services..."
docker-compose --project-name mip down

echo -e "\nDeploy Services..."
docker-compose --project-name mip up -d
