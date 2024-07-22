#!/bin/env bash

docker-compose --env-file ../.versions_env down
docker-compose --env-file ../.versions_env up -d

echo -n "Installing pip requirements ..."
pip install -r requirements.txt

echo -n "Waiting for containers to start ..."
sleep 10

echo -n "Loading data into global db ..."
docker exec dev_exareme2_global_mipdb_1 mipdb init
docker exec dev_exareme2_global_mipdb_1 mipdb load-folder /opt/data

echo -n "Loading data into local db ..."
docker exec dev_exareme2_local_mipdb_1 mipdb init
docker exec dev_exareme2_local_mipdb_1 mipdb load-folder /opt/data

echo -n "Waiting for exareme2 to see the data ..."

counter=0

while [ $counter -lt 20 ]
do
  PATHOLOGIES=$(curl -s 172.17.0.1:8080/services/pathologies)
  if [[ "$PATHOLOGIES" == *"desd-synthdata"* &&
        "$PATHOLOGIES" == *"ppmi"* &&
        "$PATHOLOGIES" == *"edsd"* &&
        "$PATHOLOGIES" == *"dementia"* &&
        "$PATHOLOGIES" == *"demo"* &&
        "$PATHOLOGIES" == *"dummy_tbi"*
  ]];
  then
    echo "Data found!"
    break
  fi

  echo -n "."
  sleep 2
  ((counter++))
done

if [ $counter -eq 20 ]; then
    echo "Reached maximum number of attempts, data not found."
fi


echo -e "\nEnter MIP at http://172.17.0.1/"
