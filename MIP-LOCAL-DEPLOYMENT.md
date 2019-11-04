# MIP-LOCAL- Deployment Guide

## Introduction

The deployment process is divided into different parts along with the different software stacks that need to be deployed. The services that will be deployed are:


1. Exareme
2. Web-Analytics-Pack


This guide will assist you in deploying all the packs together and explain what dependencies each one has with the rest. This guide does not include detailed installation steps for each service but will prompt you to the appropriate guide.

## Requirements

Each software stack has it's own requirements but in order to deploy everything into one machine you need at least 16 GB of ram.

All of the software stack is based on docker so you need to install it in the machines that you will use:

- docker (tested using version 17.05.0-ce)
- docker-compose (tested using version 1.17.0)

Each software stack has more specific requirments

## Deployment

### 1. Install Exareme

You can install exareme locally by following this guide:
[Local exareme Deployment Guide](https://github.com/madgik/exareme/tree/master/Local-Deployment)

In the next steps you will need to provide the IP of the master node of EXAREME_IP which will be refered as EXAREME_URL so keep that in mind.
### 2. Install Front-end and Backend -Pack
Clone this repository in your machine where it will be installed.

#### Initialize the variables

In order to deploy the Frontend and backend  Pack you need:

1. `EXAREME_URL` (`EXAREME_IP`:`EXAREME_PORT` from step 1 e.g. http://155.105.200.235:9090 )

Go to the `docker-compose.yml` file and modify these env variables with the values that you have from the previous steps. You can also modify the images of the portal-backend and the portal-frontend depending on what you want to deploy.

#### Setup the pathologies

Go to the `data` folder and there you will find a `pathologies.json` file.

This is used to inform the frontend what are the available datasets and CDEs. Modify this file accordingly before deploying.

#### Deploy

Run the `./run.sh` command to install the rest of the components.

After the installation is done, MIP will be visible on localhost.
