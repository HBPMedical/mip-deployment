#!/bin/env bash

docker compose --env-file ../.versions_env down
rm ../data/local.db
rm ../data/global.db
