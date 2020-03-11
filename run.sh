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

# CSVs and metadata validation
echo "Validating if the CSVs match with the metadata..."
chmod 775 config/convert-csv-dataset-to-db.py

# Removing previous .db files
rm -rf data/**/*.db

# Running the database creation script
python config/convert-csv-dataset-to-db.py -f data/ -t "master"

# Get the status code from previous command
py_script=$?

# If status code != 0 an error has occurred
if [[ ${py_script} -ne 0 ]]; then
    echo -e "\nThe CSVs could not be parsed using the metadata. Exiting..." >&2
    exit 1
else
    echo -e "\nThe CSVs match with the metadata."
fi

echo -e "\nRemoving previous services..."
docker-compose --project-name mip down

echo -e "\nDeploy Services..."
docker-compose --project-name mip up -d
