#!/bin/env bash

cat .env >> .env_with_versions
cat  ../.versions_env >> .env_with_versions

cd backend_components/
docker-compose --env-file ../.env_with_versions down
docker-compose --env-file ../.env_with_versions up -d
echo "Installing dependencies..."
poetry install
sleep 60
poetry run inv setup-dbs

cd ../
cd frontend_components/
docker-compose --env-file ../.env_with_versions down
docker-compose --env-file ../.env_with_versions up -d

cd ../
rm .env_with_versions

echo -n "Waiting for the containers to be ready..."

while true
do
  PATHOLOGIES=$(curl -s 172.17.0.1:8080/services/pathologies)
  if [[ "$PATHOLOGIES" == *"desd-synthdata"* &&
        "$PATHOLOGIES" == *"ppmi"* &&
        "$PATHOLOGIES" == *"edsd"* &&
        "$PATHOLOGIES" == *"fake_longitudinal"* &&
        "$PATHOLOGIES" == *"demo"* &&
        "$PATHOLOGIES" == *"dummy_tbi"*
  ]];
    then
	    break
  fi
  echo -n "."
  sleep 1
done
echo -e "\nEnter MIP at http://172.17.0.1/"
