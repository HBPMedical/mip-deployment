# MIP-LOCAL- Deployment Guide

## Introduction

The main objective of this project is to provide you with the information and guidance needed to successfully install the M
IP Version 5.0 in a
### demonstration setting:
    • MIP Frontend
    • MIP APIs
    • MIP EXAREME engine
    • MIP Algorithms
    • MIP Initial Metadata (Common Data Elements for one or more medical condition)
    • MIP Datasets (standard datasets and demonstration datasets)
This project is defined to set up two sets of metadata and datasets for the following medical conditions:

    • Dementia
    • Trauma Brain Injury
This project does not cover the installation of the additional data pre-processing tools (Data Factory) needed to prepare your own datasets and metadata, nor the installation of your own local datasets and associated metadata describing the specific variables you would like to focus on.  These topics will soon be covered by additional projects to be published and announced later.
The installation process of the MIP Version 5.0 in a demonstration setting is divided into different parts along with the different software stacks that need to be deployed. The MIP installation is performed in 2 major steps:
    1. Installation of the EXAREME and Backend components
    2. Installation of the Frontend components (Web-Analytics-Pack)
This guide will assist you in deploying all the packs and explain what dependencies each one has with the rest. This guide does not include detailed installation steps for each service but will prompt you to the appropriate guide.

## Prerequisites

The server must be set up according to the MIP Technical Requirements and must be in a clean state.  In case you already have a previous version of the MIP installed and before proceeding with the MIP version 5.0 installation you will need to uninstall the previous version totally. Please proceed manually to clean up the server by removing components like: MESOS, Marathon, Zookeeper.

## Installation Steps
### Before you start (requirements)
Ensure you have GIT installed on your server. If not proceed with GIT installation. When this is done:
    • clone this repository on your server so you can use it to install the MIP 5.0
    • Execute the script “after-git-clone.sh”
Each software stack has its own requirements but in order to deploy everything onto your servers you need at least 16 GB of ram.
Each software stack is based on docker and uses docker compose so you need to install docker and docker compose on your server:
    • docker (tested using version 17.05.0-ce)
    • docker-compose (tested using version 1.17.0)

Each software stack has it's own requirements but in order to deploy everything into one machine you need at least 16 GB of ram.

All of the software stack is based on docker so you need to install it in the machines that you will use:

- docker (tested using version 17.05.0-ce)
- docker-compose (tested using version 1.17.0)

## Install EXAREME and backend components
Each software stack has more specific requirments

To install EXAREME locally see the [Local exareme Deployment Guide](https://github.com/madgik/exareme/tree/master/Local-Deployment)
## Install Front End and APIs Pack

### Initialize the variables
In order to deploy the Web Analytics Pack you need:

EXAREME_URL (EXAREME_IP:EXAREME_PORT from step 1 e.g. http://155.105.200.235:9090 )

Go to the docker-compose.yml file and modify these env variables with the values that you have from the previous steps. You can also modify the images of the portal-backend and the portal-frontend depending on what you want to deploy.

### Deploy
Run the ./run.sh command to install the rest of the components.

After the installation is done, MIP will be visible on localhost.


## Verify the MIP 5.0 is working
After the installation is done, the MIP Version 5.0 in a demonstration setting is now visible on localhost.  To verify all is working fine  Launch the MIP
  Check 2 medical conditions (dementia and TBI) are accessible from the frontend
  Check 5 datasets are accessible from the front end
  ADNI, PPMI, EDSD
  Demo-DEM, Demo-TBI

