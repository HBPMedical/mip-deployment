#!/bin/env bash
set -a
source ./.versions_env
source ./.env
set +a

docker compose down -v
docker compose up -d
