# Federated MIP Deployment
## Structure
![MIP Federated Deployment](MIP_Federated_Deployment_II.png)

The federated MIP is meant to run on different VM/Physical servers (nodes):

* A **Pusher** (*4*)
* A **Master** (*5*)
* A **UI** (*6*)
* Some **Workers** (*7*)

As the *pusher* service can run on any node, the bare minimum number of required servers is 3. As the opposite as a *local* MIP setup, all the required components are not in this *mip-deployment* repository (*1*).  
As an additional part, for all the backend requirements, we will need *exareme* repository (*2*) content, and another component which is provided as an external service: the global *HBP* keycloak's instance (*5*).  
It means that the federated MIP is not meant (at least not at the moment) to run as an independant MIP setup, which you may already use with the local MIP.  

### Pusher (*4*)
The **Pusher** will contains all the *exareme* repository (*2*) structure. Its role will be to "push" containers and configurations to the **Master** and the **Worker** nodes, and to initiate a Docker Swarm network from the **Master**.  
This pusher will need to have an *ssh* access to the master and the workers, and this will also include *root* access there.  
As a Docker Swarm network is quite complicated in terms of layer 3 network protocols and layer 4 TCP and UDP port requirements, it is highly recommended to run all the different nodes in the same network subnet. That's why, if you need to have remote **Worker** nodes in hospitals, it's better to build a VPN connectivity between all the nodes.

### Master (*5*)
The **Master** will "schedule" the **Workers**. This will be the main Docker Swarm network component, the Swarm Master.  
The Docker containers running on this machine will be *exareme-master* and *exareme-keystore*.

### UI (*6*)
The **UI** will contain most of the MIP Docker containers, but it won't have any *exareme* nor *keycloak* related containers.  
This node will require a TCP connection with the **Master** node only (not mentioning external keycloak's instance).
This *mip-deployment* repository (*1*) includes a "Federation" subfolder with another *docker-compose.yml* file, which contains references to the different Docker images (hosted on Docker Hub (*2*)) (and their version tag) required to run the **UI** node only!

### Workers (*7*)
The **Worker** nodes (at least one) will have to host actual node (hospital) related datasets, and will run *exareme* container only.

## Requirements

## Setup
1. Prepare a VM/Physical machine with **Ubuntu 20.04** server
2. As root:

        adduser mipadmin
        adduser mipadmin sudo
        mkdir /opt/mip
        chown mipadmin.mipadmin /opt/mip

3. As mipadmin:

        cd /opt/mip
        git clone https://github.com/HBPMedical/mip-deployment
        cd
        sudo ln -s /opt/mip/mip-deployment/mip /usr/local/bin/
        mip install

## Run
You can then launch the MIP with:

        mip start

The first time, it will launch the configuration procedure. Then, it won't ask you anything anymore, but you can still use the following command to reconfigure things:

        mip configure

At anytime, you can learn how to use the *mip* commands with:

        mip --help
