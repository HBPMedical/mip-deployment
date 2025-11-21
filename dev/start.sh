#!/bin/env bash

docker compose --env-file .versions_env down
docker compose --env-file .versions_env up -d

echo -n "Waiting for containers to start ..."
sleep 10

echo -n "Loading data into exareme2 db ..."
docker exec dev-exareme2_global_mipdb-1 mipdb init
docker exec dev-exareme2_local_mipdb-1 /bin/bash -c "mipdb init && mipdb load-folder /opt/data"

sleep 20

echo -n "Triggering engine to see the added pathologies ..."
curl -X POST 172.17.0.1:5000/wla

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
  echo -e "\nEnter MIP at http://172.17.0.1/"
else
  echo "Data not found! Data importation failed!"
fi

