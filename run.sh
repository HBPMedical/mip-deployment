#!/usr/bin/env bash

set -e

get_script_dir () {
     SOURCE="${BASH_SOURCE[0]}"

     while [ -h "$SOURCE" ]; do
          DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
          SOURCE="$( readlink "$SOURCE" )"
          [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
     done
     cd -P "$( dirname "$SOURCE" )"
     pwd
}

cd "$(get_script_dir)"

if pgrep -lf sshuttle > /dev/null ; then
  echo "sshuttle detected. Please close this program as it messes with networking and prevents Docker links to work"
  exit 1
fi

if [ $NO_SUDO ]; then
  DOCKER="docker"
  DOCKER_COMPOSE="docker-compose"
elif groups "$USER" | grep &>/dev/null '\bdocker\b'; then
  DOCKER="docker"
  DOCKER_COMPOSE="docker-compose"
else
  DOCKER="sudo docker"
  DOCKER_COMPOSE="sudo docker-compose"
fi

for param in "$@"
do
  if [ "--no-frontend" == "$param" ]; then
    no_frontend=0
    echo "INFO: --no-frontend option detected !"
    break;
  fi
done

echo "Remove old running containers (if any)..."
$DOCKER_COMPOSE kill
$DOCKER_COMPOSE rm -f

echo "Deploy a Postgres server and wait for it to be ready..."
$DOCKER_COMPOSE up -d db zookeeper
$DOCKER_COMPOSE run wait_zookeeper
$DOCKER_COMPOSE up -d mesos_master
$DOCKER_COMPOSE run wait_mesos_master
$DOCKER_COMPOSE up -d mesos_slave
$DOCKER_COMPOSE run wait_dbs

echo "Create databases..."
$DOCKER_COMPOSE run create_dbs

echo "Migrate woken database..."
$DOCKER_COMPOSE run woken_db_setup

echo "Migrate metadata database..."
$DOCKER_COMPOSE run sample_meta_db_setup

echo "Migrate features database..."
$DOCKER_COMPOSE run sample_data_db_setup

echo "Run containers..."
for i in 1 2 3 4 5 ; do
  $DOCKER_COMPOSE up -d chronos
  $DOCKER_COMPOSE run wait_chronos
  $DOCKER_COMPOSE logs chronos | grep java.util.concurrent.TimeoutException || break
  echo "Chronos failed to start, restarting..."
  $DOCKER_COMPOSE stop chronos
done

$DOCKER_COMPOSE up -d woken
$DOCKER_COMPOSE run wait_woken

$DOCKER_COMPOSE up -d wokenvalidation
$DOCKER_COMPOSE run wait_wokenvalidation

for i in 1 2 3 4 5 ; do
  $DOCKER_COMPOSE logs chronos | grep java.util.concurrent.TimeoutException || break
  echo "Chronos failed to start, restarting..."
  $DOCKER_COMPOSE stop chronos
  $DOCKER_COMPOSE up -d chronos
  $DOCKER_COMPOSE run wait_chronos
done

if [ $no_frontend ] ; then
  FRONTEND_URL=http://localhost:8000 \
  $DOCKER_COMPOSE up -d portalbackend
else
  $DOCKER_COMPOSE up -d portalbackend
  $DOCKER_COMPOSE run wait_portal_backend
  $DOCKER_COMPOSE up -d frontend
fi

echo "DONE"
