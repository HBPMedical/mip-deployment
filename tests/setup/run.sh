#!/bin/env bash

cat .env >> .env_with_versions
cat ../../.versions_env >> .env_with_versions

cd backend_components/
docker-compose down
docker-compose --env-file ../.env_with_versions up -d
poetry run inv setup-dbs

cd ..
cd frontend_components
docker-compose down
docker-compose --env-file ../.env_with_versions up -d

cd ..
rm .env_with_versions