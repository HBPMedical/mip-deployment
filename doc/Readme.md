# Local MIP Deployment
## Structure
![MIP Local Deployment](MIP_Local_Deployment.png)

In this repository, we have both local and federated (in *Federation* subfolder) MIP structures.  

The local MIP is composed by a few Docker containers (*3*).  
This *mip-deployment* repository (*1*) includes a *docker-compose.yml* file, which contains references to the different Docker images (hosted on Docker Hub (*2*)) and their version tag.  
The *mip* script will be able to manage the installation process, as well as the different administration aspects.  

Once running, by default, the client browser will arrive on a landing page which will redirect it on the local keycloak (provider as a container) instance's page for authentication (with credentials *user*:*password*). Once connected, the client browser will be redirected to the HOSTNAME:PORT set during the configuration step.  
Therefore, it's important that both the keycloak container and the client browser can reach the HOSTNAME:PORT provided as the *PUBLIC_MIP_HOST* variable.  
It means that if the MIP installation runs inside a VM which is connected via a NATted network, this HOSTNAME:PORT should be the one of the *host* (the machine which runs the hypervisor), and not the one of the *guest* (the VM).

## Requirements
Beside the basic OS requirements, everything you need to deploy a local MIP is available in this repository.
If you don't match the OS requirements, we recommend that you deploy it inside a Virtual Machine. For that purpose, you can use any hypervisor, but if you don't know much about it, Vagrant and VirtualBox should make things easier.

## Setup
1. Prepare a VM/Physical machine with **Ubuntu 20.04** server

You'll have to know on which URL, like http://<HOSTNAME>, http://<HOSTNAME>:<PORT> or http://<IP>:<PORT> you want to expose your MIP. If you're operating it inside a VM on your computer, you may use the IP of your computer, and the port on which your VM's port 80 is mapped to, like:
http://192.168.1.3:8888

2. Install the MIP

As root:

        git clone https://github.com/HBPMedical/mip-deployment
        mip-deployment/mip --quiet --yes --no-run install

3. Configure the MIP

As root:

        mip --quiet --yes --host 192.168.1.3:8888 --with-keycloak-authentication configure all

4. Consolidate data

As **mipadmin** user:

        mip --quiet data consolidate

## Run
You can then launch the MIP with:

        mip start

After launching, you should be able to browse the MIP on the URL which will be displayed. Enjoy!

At anytime, you can learn more about the *mip* commands with:

        mip --help
