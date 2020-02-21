# MIP-Local Deployment Guide 6.0

## Introduction

The main objective of this pack is to provide you with the information and guidance needed to successfully install MIP.

This pack contains two sets of metadata and data for the following medical conditions:
  - Dementia
  - Trauma Brain Injury

This pack does not contain the data pre-processing tools (Data Factory) that are used to prepare your data and metadata.

### Additional Data

If you want to add your data on your local MIP deployment, you can look in the [Data Requirements](https://github.com/madgik/exareme/blob/reorderReadme/Documentation/InputRequirements.md) for the specifications.
When you have your data ready create a new folder inside the `data` folder, with the name of your pathology and add the data/metadata inside that folder. If you want to add some data on a pre-existing pathology you can just add you csv inside that folder. Be careful though, your data have to match with the metadata in that folder.

If your data do not match the specifications of MIP, a message will be shown when installing the software.

## Prerequisites

The server must be set up according to the MIP Technical Requirements and must be in a clean state.

It should also have:
  - git 
  - docker (tested using version 17.05.0-ce)
  - docker-compose (tested using version 1.17.0)

### Deploy
Execute the `./run.sh` script to install the components.

## Verify the MIP 6.0 is working
After the installation is done, MIP will be visible on localhost.  To verify all is working fine launch MIP and 
  - Check that 2 medical conditions (dementia and TBI) are accessible from the frontend,
  - Check that 5 datasets are accessible from the front end (4 in dementia and 1 in TBI).
  
Enjoy!

