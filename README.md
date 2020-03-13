# MIP-Local Deployment Guide 6.0

## Introduction

The main objective of this pack is to provide you with the information and guidance needed to successfully install MIP.

This pack contains two sets of metadata and data for the following medical conditions:
  - Dementia
  - Trauma Brain Injury

This pack does not contain the data pre-processing tools (Data Factory) that are used to prepare your data and metadata.

### How to add Custom Data

You can follow this <a href="../documentation/NewDataRequirements.md#new-data-requirements">guide</a>.

## System Requirements

The server must be set up according to the MIP Technical Requirements and must be in a clean state.

It should also have:
  - git
  - docker (tested using version 17.05.0-ce)
  - docker-compose (tested using version 1.17.0)

### Deploy

Clone this repository.
Execute `sudo ./run.sh` script to install all the components.

## Verify the MIP 6.0 is working
After the installation is done, MIP will be visible on localhost.  To verify all is working fine launch MIP and
  - Check that 2 medical conditions (dementia and TBI) are accessible from the frontend,
  - Check that 5 datasets are accessible from the front end (4 in dementia and 1 in TBI).

Enjoy!
