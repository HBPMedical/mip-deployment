# Web-Analytics Starter

## Introduction

Launch all the web-analytics components using docker-compose.

## Requirements

Recommended harware configuration:
* 16 GB memory

## Prerequisites

You have to install (a recent version of):
* docker (tested using version 17.05.0-ce)
* docker-compose (tested using version 1.17.0)

## Usage

### Run it

Launch all the components:
`./run.sh`

Frontend developers might want to avoid running the portal-frontend:
`./run.sh --no-frontend`

### Access it

By default, the frontend will be deployed using `frontend` as a virtual-host,
so you should add `127.0.0.1 frontend` to your `/etc/hosts` file. Then you'll
be able to access the portal at http://frontend

If you use the --no-frontend configuration, you'll have to run the frontend on
`localhost:8000`. You'll find more information in the
[portal-frontend README](https://github.com/HBPMedical/portal-frontend/blob/master/README.md).
