#!/bin/env bash

cd backend_components/
docker-compose --env-file ../../.versions_env down
docker-compose --env-file ../../.versions_env up -d
echo "Installing dependencies..."
poetry install
sleep 60
poetry run inv setup-dbs

cd ../frontend_components/
docker-compose --env-file ../../.versions_env down
docker-compose --env-file ../../.versions_env  up -d

echo -n "Waiting for the containers to be ready..."

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
