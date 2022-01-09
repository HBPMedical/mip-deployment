# Medical Informatics Platform (MIP), deployment

This is the MIP main repository.

Here, you have everything to deploy and operate a *local* or a *federated* MIP.  
As this repository can be used to deploy any type of MIP, it can also just be used as an "installer", and be deleted once the MIP is installed. i.e. for a *local* installation, using the *mip* script to install the MIP will clone this repository in /opt/mip-deployment for the operating purpose, and the *mip* script will also be callable from /usr/local/bin.  
Then, if you cloned this repository in your home for the installation purpose, you don't need it any further when the install process is done.

## Requirements
### Hardware
* 40 GB HDD
* 8 GB RAM
* 2 CPU Cores

### Software
* Ubuntu Server 20.04 (minimal installation, without GUI)

## MIP Components
The "short names" listed here represent the different MIP components, as well as recognized component names by the *mip* script.
* <a href="https://github.com/HBPMedical/portal-frontend" target="_blank">frontend</a>: The "Web App"
* <a href="https://github.com/HBPMedical/gateway" target="_blank">gateway</a>: "Middleware" layer between the MIP Frontend and a federated analytic engine
* <a href="https://github.com/HBPMedical/portal-backend" target="_blank">portalbackend</a>: The "Backend API" supports the Web App
* portalbackend_db: The portal backend's database
* <a href="https://github.com/madgik/galaxy" target="_blank">galaxy</a>: The "Workflow Engine" provides the ability to unite separate algorithms into one larger one
* keycloak: The "AuthN/AuthZ" system, based on KeyCloak (this component usually doesn't run in a *federated* MIP, as an "external" KeyCloak service does the job). In case this *local* "embedded" component is used, you may need to know some details, which you can find <a href="documentation/UsersConfiguration.md">here</a>
* keycloak_db: The KeyCloak's database, required only if the *keycloak* component needs to be used
* create_dbs: The *one shot* container which creates and populates the DBs when required
* <a href="https://github.com/madgik/exareme" target="_blank">exareme_master</a>: The "Analysis Engine" offers the federated (also used by the *local* MIP) analysis capabilities
* exareme_keystore: A "Key-Value" storage service used by the different nodes (the workers and the master in a *federated* MIP, or the same machine in a *local* MIP) to store/exchange variables

## Deployment
### Local
The *local* MIP is designed to run on a single machine.  
In this context, all the MIP components (understand: containers) run on the same hypervisor.  
For the security (AuthN/AuthZ), Keycloak comes as a MIP component.

<a href="doc/Readme.md">here</a>, you can find details about deploying and operating the *local* MIP.

### Federated
The *federated* MIP is designed to run on multiple machines.  
In this context, and as we usually use an external KeyCloak service, the components which run on the same machine are less than for the *local* deployment.

<a href="Federation/doc/Readme.md">here</a>, you can find details about deploying and operating the *federated* MIP.
