# Kubernetes Deployment

## Requirements
### Hardware
#### Master node
* 60 GB HDD
* 16 GB RAM
* 4 CPU Cores

#### Worker node
* 40 GB HDD
* 8 GB RAM
* 2 CPU Cores

### Software
From now on, most of our deployments will be done with Ubuntu Server 22.04, but as we run all the MIP containers on top of microk8s (as the Kubernetes distribution), it may be possible (never tested) to run it on other operating systems, including Mac OS, and Windows.

## Components:
Now, with the Kubernetes (K8s) deployment, we have 2 main component packs, that need to be deployed, which come as Helm charts:

### The engine: [Exareme2](https://github.com/madgik/Exareme2/tree/master/kubernetes)
* [controller](https://github.com/madgik/Exareme2/tree/master/exareme2/controller)

* [monetdb](https://github.com/madgik/Exareme2/tree/master/monetdb)
* [rabbitmq](https://github.com/madgik/Exareme2/tree/master/rabbitmq)
* [node](https://github.com/madgik/Exareme2/tree/master/exareme2/node)
* [db-importer](https://github.com/madgik/Exareme2/tree/master/mipdb)

* [smpc-db](https://github.com/docker-library/mongo)
* [smpc-queue](https://github.com/docker-library/redis)
* [smpc-coordinator](https://github.com/Exareme2/tree/master/exareme2)
* [smpc_player](https://github.com/Exareme2/tree/master/exareme2)
* [smpc-client](https://github.com/madgik/Exareme2/tree/master/exareme2)

### The web app stack:
* [frontend](https://github.com/HBPMedical/portal-frontend): The "Web App" UI
* [portalbackend](https://github.com/HBPMedical/portal-backend): The "Backend API" which supports the Web App
    * Its database bootstrap script lives next to the application code (`config/scripts/bootstrap-portal-db.sh`) and the same script is vendored in this chart under `files/portalbackend-db-init.sh` so the deployment can mount it via ConfigMap without embedding a large shell block inside the template. Keeping both copies in sync lets the container image and the Helm release evolve together.
* [portalbackend_db](https://github.com/docker-library/postgres): The portal backend's database
* **External Keycloak**: Authentication is provided by an existing Keycloak realm; this chart only wires the configuration values so the UI stack can reach it.


## Taking care of the medical data
### Storing the data in the worker VMs
On each **worker** node, a folder should be created `/data/<MIP_INSTANCE_OR_FEDERATION_NAME>/<PATHOLOGY_NAME>` for
every pathology for which we will have at least one dataset.
Afterward, The dataset CSV files should be placed in their proper pathology folder.


## Configuration
Prior to deploying it (on a microk8s K8s cluster of one or more nodes), there are a few adjustments to make in `values.yaml`. Each top-level section controls a part of the stack:

* `cluster`: namespace, storage classes and whether the cluster provisions persistent volumes dynamically (`managed: true`).
* `network`: ingress/tls configuration, public hostname and whether the UI is exposed directly or through a reverse proxy (`link`).
* `frontend`, `portalbackend`, `portalbackendDatabase`: container images, storage locations (for local deployments) and component specific options.
* `keycloak`: toggles the connection parameters to the external Keycloak instance (`enabled`, `host`, `protocol`, `realm`, `clientId`).

Copy `values.yaml` to a new file (for example `my-values.yaml`) and edit it in-place. A few important knobs:

```yaml
network:
  link: proxied            # use "direct" when exposing the UI publicly
  publicHost: mip.example.org
  publicProtocol: https

keycloak:
  enabled: true
  host: iam.example.org
  protocol: https
  realm: MIP
  clientId: mipfed

portalbackend:
  service:
    exposeDebug:
      enabled: false       # switch to true to publish debugging ports through a LoadBalancer
```

The reachability diagram from the legacy profiles is still valid as a reference for deciding the correct `network.*` settings:
![MIP Reachability Scheme](../doc/MIP_Configuration.png)

### MACHINE_MAIN_IP
This is the machine's main IP address. Generally, it's the IP address of the first NIC after the local one.  
If the MIP is running on top of a VPN, you may want to put the VPN interface's IP address.  
If you reach the machine through a public IP, if this IP is **NOT** directly assigned on the machine, but is using static NAT, you still **MUST** set the **INTERNAL** IP of the machine itself!

### MACHINE_PUBLIC_FQDN
This is the public, fully qualified domain name of the MIP, the main URL on which you want to reach the MIP from the Internet. This may point:
* Directly on the public IP of the MIP, for a **direct** use case. It may be assigned on the machine or used in front as a static NAT
* On the public IP of the reverse-proxy server, for a **proxied** use case

### MACHINE_PRIVATE_FQDN_OR_IP
This is **ONLY** used in a **proxied** use case situation.  
It's actually the internal IP or address from which the reverse-proxy server "sees" (reaches) the MIP machine.

These three settings map directly to the `network` section in `values.yaml` (`publicHost`, `link`, `publicProtocol`). When running behind a reverse proxy also set `externalProtocol` to describe the protocol used between the proxy and the MIP pods.

**WARNING!**: In **ANY** case, when you use an **EXTERNAL** KeyCloak service (i.e. iam.ebrains.eu), make sure that you use the correct *CLIENT_ID* and *CLIENT_SECRET* to match the MIP instance you're deploying!

After tailoring `values.yaml` you can deploy the UI Helm chart. We still recommend deploying the engine Helm charts first, before installing the UI components.


### Microk8s installation
On a running Ubuntu (we recommend 22.04) distribution, install microk8s (we **HIGHLY** recommend to **NOT** install Docker on your Kubernetes cluster!):
```
sudo snap install microk8s
```
```
sudo adduser mipadmin
```
```
sudo adduser mipadmin sudo
```
```
sudo adduser mipadmin microk8s
```

As *mipadmin* user:
```
microk8s enable dns helm3 ingress
```
```
sudo mkdir -p /data/<MIP_INSTANCE_OR_FEDERATION_NAME>
```
```
sudo chown -R mipadmin.mipadmin /data
```

For a "federated" deployment, you may want to add nodes to your cluster. "microk8s add-node" will give you a **one-time usage** token, which you can use on a worker node to actually "join" the cluster. This process must be repeated on all the worker nodes.

### Exareme2 Deployment
* Install the repository content
  ```
  sudo git clone https://github.com/madgik/Exareme2 /opt/exareme2
  ```
  ```
  sudo chown -R mipadmin.mipadmin /opt/exareme2
  ```
* Set the variables in /opt/exareme2/kubernetes/values.yaml
    * localnodes: 1 for a "local" deployment (yes, even if it's the same machine for master and worker), or more (the number of workers, not counting the master node) for a "federated" deployment
    * credentials_location: /opt/exareme2/credentials
    * db.storage_location: /opt/exareme2/.stored_data/db
    * db.csvs_location: /data/<MIP_INSTANCE_OR_FEDERATION_NAME>
    * controller.cleanup_file_folder: /opt/exareme2/.stored_data/cleanup
    * smpc.enabled: true (if you want, and **ONLY** in case of a federated deployment, and also **ONLY** if you have at least 3 worker nodes!)
* Label the nodes

  For the master node:
  ```
  microk8s kubectl label node <MASTER_HOSTNAME> master=true
  ```
  For all the worker nodes (even on a "local" deployment where the master and the worker are the **same** machine), add *worker* and (if you want) *smpc_player* labels:
  ```
  microk8s kubectl label node <WORKER_HOSTNAME> worker=true
  ```
  ```
  microk8s kubectl label node <WORKER_HOSTNAME> smpc_player=true
  ```
* Deploy the Helm chart
  ```
  microk8s helm3 install exareme2 /opt/exareme2/kubernetes
  ```

For a more in-depth guide on deploying Exareme2, please refer to the documentation available on the [Exareme2 Kubernetes repository](https://github.com/madgik/Exareme2/blob/master/kubernetes).



### Web App Stack Components Deployment
* Install the repository content
  ```
  sudo git clone https://github.com/HBPMedical/mip-deployment /opt/mip-deployment
  ```
  ```
  sudo chown -R mipadmin.mipadmin /opt/mip-deployment
  ```
* Copy `values.yaml` to `/opt/mip-deployment/kubernetes/my-values.yaml` and tailor it to your environment.
* Deploy (or upgrade) the Helm release with your customised values
  ```
  microk8s helm3 upgrade --install mip \
    -f /opt/mip-deployment/kubernetes/my-values.yaml \
    /opt/mip-deployment/kubernetes
  ```

# MicroK8s Automatic Recoverability

## Overview
MicroK8s is designed for simplicity and resilience. One of its key features is the automatic recoverability of both federated clusters and individual local nodes.

## Automatic Recoverability in Federation
In a federated cluster setup, MicroK8s ensures high availability and fault tolerance. If the master node in a federation faces downtime or operational issues, MicroK8s is designed to automatically recover its state and functionality.

### Key Points:
- **Self-healing Mechanism**: MicroK8s employs a self-healing mechanism that triggers upon detecting issues with the master node.
- **State Restoration**: Automatically restores the master node to its last known healthy state without manual intervention.

## Local Node Recoverability
For individual local nodes, MicroK8s offers a robust recovery process. This process is vital in scenarios where local nodes experience disruptions.

### Key Points:
- **Node Health Monitoring**: Continuous monitoring of node health to quickly identify any disruptions.
- **Automatic Restoration**: On reboot or reconnection, the local node automatically synchronizes and restores its state to align with the federation's current status.

## Recovery Time Frame
The recovery process in MicroK8s, whether for a federation or a local node, typically completes within a brief period.

### Expected Timeline:
- **Minimum Recovery Time**: Approximately 1 minute.
- **Maximum Recovery Time**: Up to 5 minutes, depending on the complexity and scale of the cluster.
