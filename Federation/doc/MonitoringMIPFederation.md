<a href="Readme.md#MonitoringMIPFederation">Federated MIP Deployment</a> -> `Monitoring the MIP Federation`

# Monitoring the MIP Federation
## <a id="RealTimeLogs">Real-time federation-wide logs</a>
In the *tmux* session (opened as **mipadmin** user), in the **logs** window (#1), you have a multi-pane view of each node of the federation.  
In each of them, you have the equivalent of the command *mip -f logs*, which shows the most appropriate logs (according to the node type), in "follow" mode.  
Don't try to CTRL-C the command, because it will "kill" the pane, and then, as it's configured to stay, it will be in "dead pane" mode. If it's the case, you can "respawn" it.  
For the different commands to use in the *tmux* session for this purpose, please see this <a href="OperatingMIPFederation.md#ShortTmuxUsageNotice">guide</a>.

## <a id="ExtendedMIPFederationBackendStatus">Extended MIP Federation Backend status</a>
There's a *mip* script's feature to get extended MIP federation status, at the backend side (without anything related to the Web interface).  
In the *tmux* session (opened as **mipadmin** user), in the **ms** (master) window (#3)
```
mip status
```
Note that here again, we don't necessarily need to use the *--node-type ms* parameter, as we already did the **master** node configuration, and this node type has been stored for this machine.

With this *mip status* command, you can use parameters like the *--verbose-level <VERBOSE_LEVEL>* one, to specify the amount of details you want to see.  
i.e. with a VERBOSE_LEVEL of *4*, you will see a lot of details, with all the different IPs (machines and Docker Swarm Networking IPs, Docker version, containers image name and version, deployment datetime, etc...)

## <a id="SpecificMIPFederationComponentLogs">Specific MIP Federation Component logs</a>
In the MIP <a href="OperatingMIPFederation.md#CreatingTmuxSession">*tmux* session description</a>, you saw that there's a dedicated window for each node.  
According to the node type, there are different <a href="../../README.md#Components">components</a> which run on the machine, and from which you can extract specific logs.  
In each machine **but** the pusher, you can run
```
mip --component <MIP_COMPONENT> logs
```
Alternatively, if you want to see the logs in "real-time", you can use the *-f* flag.  
You can also "limit" the lines that you wanna see with *--limit \<LINES>*.

As usual, don't hesitate to use
```
mip --help
```

In order for you to have a better understanding of the different available components for each type of node, here's a little table
|Node Type|Components|
| -- | -- |
|**worker**|*exareme*|
|**master**|*exareme-master*|
||*exareme-keystore*|
|**ui**|*frontend*|
||*gateway*|
||*portalbackend*|
||*portalbackend_db*|
||*galaxy*|
||*create_dbs*|

You can see here that *exareme-master* and *exareme-keystore* contains a dash ( **-** ) character, and not an underscore ( **_** ), as it was indicated in the <a href="../../README.md#Components">components</a> guide.  
This is because in this guide, the components are mainly the ones available in the *local* MIP, and in this specific case, the name differs a little bit.  
You can also notice that in the Federation, there's no *keycloak* or *keacloak_db* component.
