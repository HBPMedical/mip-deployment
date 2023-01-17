#!/bin/env bash

docker-compose --log-level ERROR  -f backend_components/docker-compose.yml down
docker-compose --log-level ERROR  -f frontend_components/docker-compose.yml down
