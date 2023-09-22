#!/bin/env bash

docker-compose --env-file ../.versions_env down
docker-compose --env-file ../.versions_env up -d

echo -n "Installing pip requirements ..."
pip install -r requirements.txt

echo -n "Waiting for containers to start ..."
sleep 10

echo -n "Loading data into exareme2 db ..."
docker exec dev_deployment_exareme2_mipdb_1 mipdb init
docker exec dev_deployment_exareme2_mipdb_1 mipdb load-folder /opt/data

echo -n "Waiting for exareme2 to see the data ..."

# TODO Replace never ending loop with limited attempts
while true
do
  PATHOLOGIES=$(curl -s 172.17.0.1:8080/services/pathologies)
  if [[ "$PATHOLOGIES" == *"desd-synthdata"* &&
        "$PATHOLOGIES" == *"ppmi"* &&
        "$PATHOLOGIES" == *"edsd"* &&
        "$PATHOLOGIES" == *"longitudinal_dementia"* &&
        "$PATHOLOGIES" == *"demo"* &&
        "$PATHOLOGIES" == *"dummy_tbi"*
  ]];
    then
	    break
  fi
  echo -n "."
  sleep 2
done

echo -e "\nEnter MIP at http://172.17.0.1/"
