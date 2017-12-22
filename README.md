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

## Launch

Launch all the components:
`./run.sh`

Frontend developers might want to avoid running the portal-frontend:
`./run.sh --no-frontend`
