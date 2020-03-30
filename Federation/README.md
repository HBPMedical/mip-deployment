# MIP Deployment Guide for Federation

## Introduction
Following the instructions below you will be able to deploy the whole stack of MIP.
The stack of MIP consists of:

0. Federated Exareme
1. Frontend
2. Backend
3. Galaxy

## Requirements

For the Federated Exareme make sure that you have read about <a href="https://github.com/madgik/exareme/tree/master/Federated-Deployment#requirements">requirements</a> and <a href="https://github.com/madgik/exareme/tree/master/Federated-Deployment#ports">ports</a> that need to be opened for Exareme to run as long as some optional ones for some other services like Portainer for troubleshooting.
Also, take a look at the <a href="https://github.com/madgik/exareme/blob/master/Federated-Deployment/Documentation/Federation_Specifications.md">Federation_Specifications.md</a> since it contains valid information about ports that must be open in order for Docker Swarm to run
and <a href="https://github.com/madgik/exareme/blob/master/Federated-Deployment/Documentation/Firewall_Configuration.md">Firewall_Configuration.md</a>

For the rest of the pack of MIP you will need:
- Python
- docker-compose (tested using version 1.25.4)

## Pathologies
The data management team is responsible for creating and maintaining ```pathologies.json``` file for Federated MIP. Place the file inside ```Federation/config/``` folder.

## Minimum Requirements

For the server in which Frontend, Backend and Galaxy will be deployed you may consider <a href="../README.md#minimum-requirements">these</a> minimum requirements.

If the disk space on the machine is limited consider cleaning up the old versions when they are updated, using this script:
```
sudo ./cleanUp.sh
```


## Deployment

### 1. Install Exareme

You can install Federated Exareme by following this guide:
[Federated Deployment Guide](https://github.com/madgik/exareme/tree/master/Federated-Deployment)

FYI: The one thing that you *must* remember is the IP where Exareme master will run. You will be prompted to enter that IP in the next steps.

### 2. Install Frontend, Backend and Galaxy

Clone this repository and under folder ```Federation/``` run ```sudo ./run.sh```. You will be prompted to enter the IP of the Exareme master from <a href="#1-install-exareme">1. Install Exareme</a> as long as the PUBLIC_MIP_IP which is the IP where MIP will be visible from. You can also create an ```.env``` file and place
the above IPs at the end of the file like this: </br>
```EXAREME_IP=X.X.X.X```</br>
```PUBLIC_MIP_IP=Y.Y.Y.Y```.
