#!/bin/env bash

docker-compose -f backend_components/docker-compose.yml down
docker-compose -f frontend_components/docker-compose.yml down
