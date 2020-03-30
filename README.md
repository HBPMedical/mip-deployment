# MIP Deployment Guide for Local

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

Please *mind* that with the above requirements, if you need to re-deploy because of *new Software versions*, there is an extra step you need to make if your disk space is very limited.
Execute ```sudo ./cleanUp.sh``` before ```sudo ./run.sh```

### How to add Custom Data

You can follow this <a href="./documentation/NewDataRequirements.md">guide</a>.

*You should consider adjusting the above <a href="README.md#minimum-requirements">requirements</a> with respect to your additional data size.*

### System Requirements

The server must be set up according to the MIP Technical Requirements and must be in a clean state.

It should also have:
  - git
  - docker (tested using version 17.05.0-ce)
  - docker-compose (tested using version 1.17.0)
  - python (2.7)

If you want your MIP installation to be accessible externally you should follow this ports configuration <a href="./documentation/PortsConfiguration.md">guide</a>.

## Deploy

Clone this repository.
Execute `sudo ./run.sh` script to install all the components.

## Test

After the installation is done, MIP will be visible on localhost. To verify everything is working properly go to http://localhost and
  - Check that 2 medical conditions (dementia and TBI) are visible,
  - and that 5 datasets are accessible (4 in dementia and 1 in TBI).

You can login with the default user:
```
username: user
password: password
```

If everything is working properly you should configure the users following this <a href="./documentation/UsersConfiguration.md">guide</a>.

Enjoy!

## Troubleshooting

<b>Problem:</b> </br>
*If at any point during the execution of the script, while docker networks (mip_backend,mip_frontend) are created, encounter this error:*</br>
```Creating network "mip_*" with the default driver
ERROR: Failed to program FILTER chain: iptables failed: * DOCKER: iptables v1.6.1: Couldn't load target `DOCKER':No such file or directory

Try `iptables -h' or 'iptables --help' for more information.
 (exit status 2)
```

<b>Solution:</b> </br>
```sudo systemctl restart docker```
