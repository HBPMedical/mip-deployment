#!/usr/bin/env bash

SCRIPTDIR=`dirname "$0"`

cd $SCRIPTDIR

./stop.sh

docker image rm $(docker images --filter=reference='hbpmip/*' -q)