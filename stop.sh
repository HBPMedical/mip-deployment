#!/usr/bin/env bash

if groups "$USER" | grep &>/dev/null '\bdocker\b'; then
  DOCKER_COMPOSE="docker-compose --project-name webanalyticsstarter"
else
  DOCKER_COMPOSE="sudo docker-compose --project-name webanalyticsstarter"
fi

export HOST=$(hostname)

$DOCKER_COMPOSE down
$DOCKER_COMPOSE rm -f
