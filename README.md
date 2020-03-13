# MIP-Local Deployment Guide 6.0

## Introduction

The main objective of this pack is to provide you with the information and guidance needed to successfully install MIP.

This pack contains two sets of metadata and data for the following medical conditions:
  - Dementia
  - Trauma Brain Injury

This pack does not contain the data pre-processing tools (Data Factory) that are used to prepare your data and metadata.

### Minimum Requirements

Here you will find the minimum requirements that *had been tested* with the `data` folder existing in that repo:

- 2 Core CPU
- 4 GB RAM
- 16 GB Disk
- Ubuntu 18.04 Ubuntu
- Docker version: 19.03
- Docker-compose version: 1.25.4

Please *mind* that with the above requirements If you need to re-deploy because of *new Software versions*, there is an extra step you need to make in order for some Disk space to clean up since it is limited.
Execute ```sudo ./cleanUp.sh``` before ```sudo ./run.sh```

The script ```cleanUp.sh``` will *stop* every container running for MIP Local, *remove* every image that had been stored in the machine to make space for the newer images that will be stored with
the re-deploy of new Software versions. This is needed because Docker will not remove any images automatically even if it will run newer versions of the existing images.

### Additional Data

If you want to add your data on your local MIP deployment, you can look in the [Data Requirements](https://github.com/madgik/exareme/blob/master/Documentation/InputRequirements.md) for the specifications.
When you have your data ready create a new folder inside the `data` folder, with the name of your pathology and add the data/metadata inside that folder. If you want to add some data on a pre-existing pathology you can just add you csv inside that folder. Be careful though, your data have to match with the metadata in that folder.

If your data do not match the specifications of MIP, a message will be shown when installing the software.

*You should consider adjusting the above <a href="README.md#minimum-requirements">requirements</a> with respect to your additional data size.*

## Prerequisites

The server must be set up according to the MIP Technical Requirements and must be in a clean state.

It should also have:
  - git
  - docker (tested using version 17.05.0-ce)
  - docker-compose (tested using version 1.17.0)

### Deploy
Clone this repository.
Execute `sudo ./run.sh` script to install the components.

## Verify the MIP 6.0 is working
After the installation is done, MIP will be visible on localhost.  To verify all is working fine launch MIP and
  - Check that 2 medical conditions (dementia and TBI) are accessible from the frontend,
  - Check that 5 datasets are accessible from the front end (4 in dementia and 1 in TBI).

Enjoy!
