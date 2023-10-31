# Medical Informatics Platform (MIP), Kubernetes deployment

With a whole new way of deploying the MIP, come new requirements, recommendations, and maybe constraints as well.
Also, there's a will a "merge" the *local* and *federated* deployments.
Now, everything can be deployed on Kubernetes, without the need to use the Docker engine anymore.

## Requirements
### Hardware
#### Master
* 60 GB HDD
* 16 GB RAM
* 4 CPU Cores

#### Worker node
* 40 GB HDD
* 8 GB RAM
* 2 CPU Cores

### Software
From now on, most of our deployments will be done with Ubuntu Server 22.04, but as we run all the MIP containers on top of microk8s (as the Kubernetes distribution), it may be possible (never tested) to run it on other operating systems, including Mac OS, and Windows.

## <a id="Components">MIP Components</a>
Now, with the Kubernetes (K8s) deployment, we have 3 main, big components, which come as Helm charts:

### [Exareme2](https://github.com/madgik/Exareme2/tree/master/kubernetes) (Exareme 2)
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

<a id="UI"></a>
### [UI](doc/Readme.md)
* [frontend](https://github.com/HBPMedical/portal-frontend): The "Web App"
* [gateway](https://github.com/HBPMedical/gateway): "Middleware" layer between the MIP Frontend and a federated analytic engine
* [gateway_db](https://github.com/docker-library/postgres): The gateway's database
* [portalbackend](https://github.com/HBPMedical/portal-backend): The "Backend API" which supports the Web App
* [portalbackend_db](https://github.com/docker-library/postgres): The portal backend's database
* [keycloak](https://github.com/keycloak/keycloak-containers): The "AuthN/AuthZ" system, based on KeyCloak (this component usually doesn't run in a *federated* MIP, as an "external" KeyCloak service does the job). In case this *local* "embedded" component is used, you may need to know some <a id="UsersConfiguration">details</a>, which you can find [here](documentation/UsersConfiguration.md)
* [keycloak_db](https://github.com/docker-library/postgres): The KeyCloak's database, required only if the *keycloak* component needs to be used
* [create_dbs](https://github.com/HBPMedical/docker-create-databases): The *one shot* container which creates and populates the DBs when required

For deployment documentation, go [here](doc/Readme.md).
