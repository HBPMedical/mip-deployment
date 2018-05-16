#!/usr/bin/env bash

#
# Start Woken in a distributed mode with its full environment and two worker nodes using different datasets.
#
# Option:
#   --no-tests: skip the test suite
#   --all-tests: execute the full suite of tests, including slow tests such as Chaos testing
#   --no-frontend: do not start the frontend
#

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
  DOCKER_COMPOSE="docker-compose -f docker-compose-federation.yml"
elif groups "$USER" | grep &>/dev/null '\bdocker\b'; then
  DOCKER="docker"
  DOCKER_COMPOSE="docker-compose -f docker-compose-federation.yml"
else
  DOCKER="sudo docker"
  DOCKER_COMPOSE="sudo docker-compose -f docker-compose-federation.yml"
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
$DOCKER_COMPOSE run sample_data_db_setup1
$DOCKER_COMPOSE run sample_data_db_setup2

echo "Run containers..."
for i in 1 2 3 4 5 ; do
  $DOCKER_COMPOSE up -d chronos
  $DOCKER_COMPOSE run wait_chronos
  $DOCKER_COMPOSE logs chronos | grep java.util.concurrent.TimeoutException || break
  echo "Chronos failed to start, restarting..."
  $DOCKER_COMPOSE stop chronos
done

$DOCKER_COMPOSE up -d wokennode1 wokennode2
$DOCKER_COMPOSE run wait_wokennode1
$DOCKER_COMPOSE run wait_wokennode2
$DOCKER_COMPOSE up -d wokenvalidationnode1 wokenvalidationnode2
$DOCKER_COMPOSE run wait_wokenvalidationnode1
$DOCKER_COMPOSE run wait_wokenvalidationnode2

$DOCKER_COMPOSE up -d wokencentral
$DOCKER_COMPOSE run wait_wokencentral

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
