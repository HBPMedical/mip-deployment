#!/bin/env bash

docker-compose --env-file ../.env_with_versions -f backend_components/docker-compose.yml down
docker-compose --env-file ../.env_with_versions -f frontend_components/docker-compose.yml down
