![Home](../README.md) -> `Federated MIP Deployment`

# Federated MIP Deployment
## Structure
![MIP Federated Deployment](MIP_Federated_Deployment_II.png)

The federated MIP is meant to run on different VM/Physical servers (nodes):

* A **Pusher** (*4*)
* A **Master** (*5*)
* A **UI** (*6*)
* Some **Workers** (*7*)

As the *pusher* service can run on any node, the bare minimum number of required servers is 3. That said, it's still strongly encouraged to deploy a pusher on a dedicated server.  
As the opposite as a *local* MIP setup, all the required components are not in this *mip-deployment* repository (*1*).  
As an additional part, for all the backend requirements, we will need the *exareme* repository (*2*) content, and another component (provided as an external service) which is the global *HBP* KeyCloak's instance (*5*).  
Additionally, another external service can be used in a more punctual way: the *data catalogue*.  
All these statements mean that the federated MIP is not designed (at least not at the moment) to run as an independant MIP setup.  
That said, you can deploy your own KeyCloak server and your own data catalogue, but these processes won't be documented here.

### Pusher (*4*)
The **Pusher** will contain all the *exareme* repository (*2*) structure. Its role will be to "push" containers and configurations to the **Master** and the **Worker** nodes, and to initiate a Docker Swarm network from the **Master**.  
This pusher will need to have an *ssh* access to the master and the workers, and this will also include *root* access there.  
As a Docker Swarm network is quite complicated in terms of layer 3 network protocols and layer 4 TCP and UDP port requirements, it is highly recommended to run all the different nodes in the same network subnet. That's why, if you need to have remote **Worker** nodes in hospitals, it's better to build a VPN connectivity (preferably in layer 2) between all the nodes. Such a VPN setup won't be documented here either.  
As this **Pusher** is a central actor in the federation, it's also the best candidate to initiate federated actions, like the synchronization (consolidation) of metadata and pathologies details over the federation, the automated data compilation on the workers and master nodes, and the remote KeyCloak roles synchronization, amongst other useful features.

### Master (*5*)
The **Master** will "schedule" and "rule" the **Workers**. This will be the main Docker Swarm network component, the Swarm Master.  
The Docker containers running on this machine will be *exareme-master* and *exareme-keystore*.

### UI (*6*)
The **UI** will contain most of the MIP Docker containers, but it won't have any *exareme* nor *keycloak* related container.  
This node will require a TCP connection with the **Master** node only (not mentioning the external KeyCloak's instance, nor the reference to the external data catalogue).  
This *mip-deployment* repository (*1*) includes a "Federation" subfolder with another *docker-compose.yml* file, which contains the references to the different Docker images (hosted on Docker Hub (*2*)) and their version tag, required to run the **UI** node only!  
As this node will actually run the user Web interface, it will be the only one which is required to be reachable via HTTP/HTTPS.

### Workers (*7*)
The **Worker** (usually located in hospital premises) nodes (at least one) will have to host the actual node-related datasets, and will run the *exareme* container only.

## Requirements
For the different nodes, the requirements are the same as for a local MIP.

### Hardware
* 40 GB HDD
* 8 GB RAM
* 2 CPU Cores

### Software
* Ubuntu Server 20.04 (minimal installation, without GUI).  

## Setup
### Preparing the machines
Prepare a VM/Physical machine with **Ubuntu Server 20.04** (basic OS, without GUI), for each node of the federation. As we want to be able to run federated data analysis, we'll typically go with two workers, with the following plan:

* **pusher**
* **ms** (master)
* **ui** (frontend)
* **wk1** (worker 1)
* **wk2** (worker 2)

On every node **but** the pusher, we'll use the *mip-deployment* repository as an installer. Then, once installed, the *mip* script will (by default) delete the installer folder.  
In the **ui** node, the installer will **re**-clone the *mip-deployment* repository, but in /opt. Therefore, after the installation has been done, it can also remove the *mip-deployment* folder that was used as the installer.  
If you want to keep the installer folder, you'll have to explicitely use the flag *--keep-installer*.

### Preparing the **worker** nodes
Follow this ![guide](PreparingWorkers.md).

### Preparing the **master** node
Follow this ![guide](PreparingMaster.md).

### Preparing the **ui** node
Follow this ![guide](PreparingUI.md).

### Preparing the **pusher** node
Follow this ![guide](PreparingPusher.md).

## Operating the MIP Federation
The first time, after the setup, just remember to follow these steps in the right order:

1. Generate the *tmux* session and connect to it
1. Consolidate the data
1. Compile the data
1. Deploy the backend services (Docker Swarm)
1. Synchronize the KeyCloak roles

You will find detailed explanations in this ![guide](OperatingMIPFederation.md).
