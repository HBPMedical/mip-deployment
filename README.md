# MIP-Local Deployment Guide v6.0.0

## Introduction

The main objective of this pack is to provide you with the information and guidance needed to successfully install the MIP Local Version 6.0.0 with all of its components that is used for demonstration purposes. It contains:
  - MIP Frontend
  - MIP APIs
  - MIP EXAREME engine
  - MIP Algorithms
  - MIP Initial Metadata (Common Data Elements for one or more medical condition)
  - MIP Datasets (standard datasets and demonstration datasets)
	
This pack contains two sets of metadata and data for the following medical conditions:
  - Dementia
  - Trauma Brain Injury

This pack does not cover the installation of the additional data pre-processing tools (Data Factory) needed to prepare your own datasets and metadata.

### Additional Data

If you want to add your data on your local MIP deployment, you can look in the [Data Requirements](https://github.com/madgik/exareme/blob/reorderReadme/Documentation/InputRequirements.md) and then go to the `data` folder, create a new folder with the name of your pathology and add the data/metadata inside that folder.

If your data do not match the specifications of MIP, a message will be shown when setting up MIP.

## Prerequisites

The server must be set up according to the MIP Technical Requirements and must be in a clean state.

It should also have:
  - git 
  - docker (tested using version 17.05.0-ce)
  - docker-compose (tested using version 1.17.0)


## TODO

  - One script deployment
  - pathologies.json should be created automatically
  - validate the data before running the deployment scripts
  - Galaxy to be included




## Install EXAREME and backend components
Each software stack has more specific requirments

To install EXAREME locally see the [Local exareme Deployment Guide](https://github.com/madgik/exareme/tree/master/Local-Deployment)
## Install Front End and APIs Pack

### Initialize the variables
In order to deploy the Web Analytics Pack you need:

EXAREME_URL (EXAREME_IP:EXAREME_PORT from step 1 e.g. http://155.105.200.235:9090 )

Go to the docker-compose.yml file and modify these env variables with the values that you have from the previous steps. You can also modify the images of the portal-backend and the portal-frontend depending on what you want to deploy.

### Setup the pathologies

Go to the `data` folder and there you will find a `pathologies.json` file.

This is used to inform the frontend what are the available datasets and CDEs. Modify this file accordingly before deploying.

### Deploy
Run the ./run.sh command to install the rest of the components.

After the installation is done, MIP will be visible on localhost.


## Verify the MIP 5.0 is working
After the installation is done, the MIP Version 5.0 in a demonstration setting is now visible on localhost.  To verify all is working fine  Launch the MIP
  Check 2 medical conditions (dementia and TBI) are accessible from the frontend
  Check 5 datasets are accessible from the front end
  ADNI, PPMI, EDSD
  Demo-DEM, Demo-TBI

