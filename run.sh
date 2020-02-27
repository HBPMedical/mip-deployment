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

echo "Starting the process of creating databases.."
chmod 775 convert-csv-dataset-to-db.py
#Removing all previous .db files from the data/
echo -e "\nDeleting previous databases."
rm -rf data/**/*.db

echo "Parsing CSV files from data/ to database files. "
python convert-csv-dataset-to-db.py -f data/ -t "master" 2> /dev/null
#Get the status code from previous command
py_script=$?
#If status code != 0 an error has occurred
if [[ ${py_script} -ne 0 ]]; then
     echo "Creation of databases failed. Exiting.." >&2
     exit 1
fi

echo -e "\nRemoving previous services..."
docker-compose --project-name mip down

echo -e "\nDeploy Services..."
docker-compose --project-name mip up -d
