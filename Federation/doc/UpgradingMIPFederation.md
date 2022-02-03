[Federated MIP Deployment](Readme.md#UpgradingMIPFederation) -> `Upgrading the MIP Federation`

# Upgrading the MIP Federation
## <a id="UpgradingPusher">Upgrading the **pusher** node</a>
### Check-list
* Connect to the **pusher** node as *mipadmin*
* If you're in the *tmux* session, detach it, prior to upgrading the node
* Make sure you're not in the *exareme* deployment folder
  ```
  cd
  ```

### Installing the new version of the *mip* script
```
git clone https://github.com/HBPMedical/mip-deployment
```
```
sudo mip-deployment/mip --pusher --federation <FEDERATION_NAME> --self --force install
```
As it was already explained in the [**pusher** preparation](PreparingPusher.md), there are other parameters you can use here to install another specific version of the *MIP* (and they can be used in the case of the *mip script* install as well).

#### Cleanup
```
rm -rf mip-deployment
```

### Installing the new *MIP* version
```
sudo mip --pusher --federation <FEDERATION_NAME> install
```
Again, as explained in the [**pusher** preparation](PreparingPusher.md), if you have to install a specific version, use the documented parameters, and don't hesitate to call *mip --help*.

When upgrading a **pusher** or **ui** node, a backup of the current installation is made. Then, the current installation folder is deleted, the new one is cloned from github, and finally, the backup is automatically restored.

### Fixing the pre-6.5 folders after the automatic restore
When upgrading to *MIP 6.5* from an older version, there's a breaking change in the *exareme* deployment folder, which means that the restore will result in some folders being put in the wrong place. Let's fix it:

```
sudo cp -r /opt/<FEDERATION_NAME>/exareme/Federated-Deployment/Compose-Files /opt/<FEDERATION_NAME>/exareme/Federated-Deployment/docker-swarm/
```
```
sudo rm -r /opt/<FEDERATION_NAME>/exareme/Federated-Deployment/Compose-Files
```
```
sudo cp -r /opt/<FEDERATION_NAME>/exareme/Federated-Deployment/Docker-Ansible /opt/<FEDERATION_NAME>/exareme/Federated-Deployment/docker-swarm/
```
```
sudo rm -r /opt/<FEDERATION_NAME>/exareme/Federated-Deployment/Docker-Ansible
```

### Fixing the configuration/permissions
```
sudo mip --pusher --federation <FEDERATION_NAME> configure all
```

You can now reconnect the tmux session to work on the other nodes
```
mip --pusher --federation <FEDERATION_NAME> tmux
```

## <a id="UpgradingMaster">Upgrading the **master** node</a>
### Check-list
* In the *tmux* session (opened as **mipadmin** user), go in the **ms** (master) window (#3)

### Installing the new version of the *mip* script
```
git clone https://github.com/HBPMedical/mip-deployment
```
```
sudo mip-deployment/mip --self --force install
```
As it was already explained in the [**master** preparation](PreparingMaster.md), there are other parameters you can use here to install another specific version of the *MIP* (and they can be used in the case of the *mip script* install as well).

#### Cleanup

```
rm -rf mip-deployment
```

### Installing the new *MIP* version
```
sudo mip --node-type ms install
```
Again, as explained in the [**master** preparation](PreparingMaster.md), if you have to install a specific version, use the documented parameters, and don't hesitate to call *mip --help*.

## <a id="UpgradingUI">Upgrading the **ui** node</a>
### Check-list
* In the *tmux* session (opened as **mipadmin** user), in the **ui** window (#4)
* Make sure you're not in the *mip-deployment* folder
  ```
  cd
  ```

### Installing the new version of the *mip* script
```
git clone https://github.com/HBPMedical/mip-deployment
```
```
sudo mip-deployment/mip --self --force install
```
As it was already explained in the [**ui** preparation](PreparingUI.md), there are other parameters you can use here to install another specific version of the *MIP* (and they can be used in the case of the *mip script* install as well).

#### Cleanup

```
rm -rf mip-deployment
```

### Installing the new *MIP* version
```
sudo mip --node-type ui install
```
Again, as explained in the [**ui** preparation](PreparingUI.md), if you have to install a specific version, use the documented parameters, and don't hesitate to call *mip --help*.

## <a id="UpgradingWorkers">Upgrading the **wk** nodes</a>
In the *tmux* session (opened as **mipadmin** user), do this in each worker windows (#5-#n)

### Installing the new version of the *mip* script
```
git clone https://github.com/HBPMedical/mip-deployment
```
```
sudo mip-deployment/mip --pusher --federation <FEDERATION_NAME> --self --force install
```
As it was already explained in the [**workers** preparation](PreparingWorkers.md), there are other parameters you can use here to install another specific version of the *MIP* (and they can be used in the case of the *mip script* install as well).

#### Cleanup
```
rm -rf mip-deployment
```

### Installing the new *MIP* version
```
sudo mip --node-type wk install
```
Again, as explained in the [**workers** preparation](PreparingWorkers.md), if you have to install a specific version, use the documented parameters, and don't hesitate to call *mip --help*.

## <a id="Redeploying">Redeploying</a>
### Detach the *tmux* session
```
CTRL+j d
```

### Regenerate the *tmux* session
```
mip --pusher --federation <FEDERATION_NAME> --force tmux
```

### Stop the services
In the *tmux* session (opened as **mipadmin** user), in the **pusher** window (#0)
```
mip --pusher --federation <FEDERATION_NAME> service stop
```

### Deploy the services
Still in the window #0
```
mip --pusher --federation <FEDERATION_NAME> service deploy
```
