## Backup and Recovery

### Kubernetes volume folders

MIP is currently deployed using kubernetes and the data that need to be persisted are mounted in volumes.
The data that need to be persisted are located ONLY in the central node.

The volumes that are created in the host machine can be seen [here](../kubernetes/values.yaml) as storage data paths.

The folders that currently need to be backed up are the following:
1. The portal-backend stored data under `/opt/mip-deployment/.stored_data`
2. The config folder under `/opt/mip-deployment/config`

### Backup
Backing up the aforementioned folders is enough for saving all important information.
Any packaging or compression can be used after the folders have been extracted.

The services DO NOT need to be stopped to create the backup.


### Recovery
For the recovery operation the following steps are needed:
1. The services need to be stopped. 
2. If any data from the services exist in the mounted folders, they need to be removed. 
Only the backup information will be restored, we cannot merge different states.
3. The backup is moved to the mounted folders, accordingly. 
4. The services are started.
