<a href="Readme.md#OperatingMIPFederation">Federated MIP Deployment</a> -> `Operating the MIP Federation`

# Operating the MIP Federation
## <a id="GeneratingTmuxSession">Using the *tmux* session</a>
*tmux* is a virtual console, which will continue to live on the **pusher**, even if you disconnect your current session. Anytime you may need to operate the federation, you will have to open an SSH session on the **pusher**, and **re**-attach to the *tmux* session. Then, when you're done and you want to disconnect, first detach the *tmux* session, then close your SSH connection.  

### <a id="ShortTmuxUsageNotice">Short *tmux* usage notice</a>
We won't detail the *tmux* usage here, but as a short notice:

* When you're outside (not attached to) a *tmux* session
  * List all the available *tmux* sessions (before you attach a session)
    ```
    tmux ls
    ```
  You will see the different sessions name or id.
  * Attach to a *tmux* session
    ```
    tmux a -t <SESSION_ID>
    ```
* When you're inside (attached to) a *tmux* session
  * Any operation will have to begin with *CTRL + j* (usually *CTRL + b*, but to avoid issues when having *tmux* inside *tmux* inside *tmux*, all the generated MIP-related *tmux* sessions have been redefined with *CTRL + j*)
  * Detach the *tmux* session
    ```
    "CTRL + j" d
    ```
  * Navigate to the *next* window inside the session
    ```
    "CTRL + j" n
    ```
  * Navigate to the *previous* window inside the session
    ```
    "CTRL + j" p
    ```
  * Directly jump to a certain window number (0-9 only)
    ```
    "CTRL + j" <WINDOW_NUMBER>
    ```
  * Navigate to the *next* pane inside a multi-panes window (like the logs window (1))
    ```
    "CTRL + j" o
    ```
    On the MIP-related generated *tmux* session, on any OS **but** Mac (currently), you can also use the *ALT + ARROW_KEYS* shortcut
  * Quickly show the pane numbers
    ```
    "CTRL + j" q
    ```
  * Directly jump to a certain pane number (0-9 only)
    ```
    "CTRL + j" q <PANE_NUMBER> (the number must be entered really quickly after the q)
    ```
  * Zoom (in or out) the currently selected pane
    ```
    "CTRL + j" z
    ```
  * Enter copy mode (to stop the live logs and go back in the pane's history)
    ```
    "CTRL + j" [
    ```
  * Quit copy mode
    ```
    q or ESC
    ```
  * Respawn a "dead" pane or window
    ```
    "CTRL + j" r
    ```
If you want to know more about *tmux*, go on the [tmux Cheat Sheet](https://tmuxcheatsheet.com).

### <a id="CreatingTmuxSession">Creating the *tmux* session</a>
Now that you know a bit more about *tmux*, we will generate the MIP special *tmux* session (or connect to it, if it already exists).  

On the **pusher** node, with the **mipadmin** user, you have to run
```
mip --pusher --federation <FEDERATION_NAME> tmux
```
This will generate the session if it does not exist, and then, in any case, attach to it.  
If you want to force **re**-generate the *tmux* session, you can use the *--force* flag.

Now that you're inside the session, you will notice that several windows are present (with *<WINDOW_NUMBER>*:*<WINDOW_NAME>* tab names). You can also notice that, left to the tab names, there's the *tmux* session's name (in blue), and it should be the <FEDERATION_NAME>.

|Window Number|Window Name|Description|
| -- | -- | -- |
|0|bash|Console on the **pusher** node|
|1|logs|Multi-panes window to display real-time logs of all the nodes (top-to-bottom, left-to-right: **master**, **ui**, then all the workers)|
|2|deploy|A quick help about the **pusher** commands to operate the main MIP Federation tasks|
|3|<FEDERATION_NAME>-ms|Console on the **master** node|
|4|<FEDERATION_NAME>-ui|Console on the **ui** node|
|5-n|<FEDERATION_NAME>-wk-<HOSPITAL_SHORT_NAME>|Console on the **worker** nodes|

## <a id="ConsolidatingData">Consolidating data</a>
In the *tmux* session (opened as **mipadmin** user), in the **pusher** window (#0):
```
mip --pusher --federation <FEDERATION_NAME> data consolidate
```
For each pathology accross the federation **workers**, this will list the different available datasets in the pathology's Common Data Elements (CDE) file, and then, from all the CDEs, it will generate the *pathologies.json* file (and push it to the **ui** node), used by the MIP Web interface to display the different variables.  
In order for you to better understand this process, here's a step-by-step action list

1. For each **worker** node

   1. Connect to the node
   1. Ask it to prepare a list of the available datasets (and for each of those, give a prototype (headers list) of the data)
   1. Download this archived list on the **pusher**
   1. For each pathology in this list, download (on the **pusher**) the corresponding CDE from the **master** node (or directly from the data catalogue, if asked via optional parameters)
1. On the **pusher** node, parse the prepared pathology list
   1. For each pathology, edit the CDE and there, list **only** the available datasets in the federation
   1. Redistribute this modified CDE on the **master** and on each participating **worker** node
   1. With all the available CDE files, "compile" the *pathologies.json* file, and push it on the **ui** node

Alternatively, you can ask to **re**-label the pathologies and/or the datasets by using the flag *--review-dataset-labels*.  
As said earlier, you can ask the script to download the CDEs from the data catalogue using the flag *--online-cdes*.  
If you want to use an non-default data catalogue, you can use the following parameters
* *--datacatalogue-protocol* (*http* | *https*)
* *--datacatalogue-host <DATACATALOGUE_URL>*

Don't hesitate to use:
```
mip --help
```

## <a id="CompilingData">Compiling data</a>
In the *tmux* session (opened as **mipadmin** user), in the **pusher** window (#0)
```
mip --pusher --federation <FEDERATION_NAME> data compile
```
At any time, you can **re**-compile by using the *--force* flag.  
You can also specify the pathology(ies) to compile, with the *--pathology \<PATHOLOGIES>* parameter (comma-separated pathologies list).  
If you want to limitate the compilation to a certain node, you can use the *--node \<NODE_NAME>* parameter, but in this case, you'll also have to pass the *--pathology* argument.  

As usual, to get more details, use:
```
mip --help
```

## <a id="DeployingServices">Deploying services</a>
In the *tmux* session (opened as **mipadmin** user), in the **pusher** window (#0)
```
mip --pusher --federation <FEDERATION_NAME> service deploy
```
This will deploy the Docker Swarm network, the master-related containers on the **master** node, and the worker container on each **worker** node.  
At any time, you can **re**-deploy by using the same command.

### Service-related additionnal features
Alternatively, there are different things that you can run in the same way (still on the **pusher** console of the *tmux* session)

* Showing the services status
  ```
  mip --pusher --federation <FEDERATION_NAME> service status
  ```
* Starting the services
  ```
  mip --pusher --federation <FEDERATION_NAME> service start
  ```
* Stopping the services
  ```
  mip --pusher --federation <FEDERATION_NAME> service stop
  ```
* Restarting the services
  ```
  mip --pusher --federation <FEDERATION_NAME> service restart
  ```
  Note that a *restart* is actually different from a "*stop* *start*" cycle. See the Docker documentation.

For all these commands (including the *deploy* one), you can use the *--node <NODE_NAME>* parameter to limitate the scope to a certain node.

As usual, to get more details, use:
```
mip --help
```

## Synchronizing the KeyCloak roles
Follow this <a id="SynchronizingKeycloakRoles" href="SynchronizingKeycloakRoles.md">guide</a>.

## Run the MIP Web Interface
In the *tmux* session (opened as **mipadmin** user), in the **ui** window (#4)
```
mip start
```
Note that here, we don't necessarily need to use the *--node-type ui* parameter, as we already did the **ui** node configuration, and this node type has been stored for this machine.

After launching, you should be able to browse the MIP on the URL which will be displayed.  
Note that once the command ends, it may still take up to one minute until the MIP's Web interface is really operational.  
Of course, you can also do other actions here:
* Stopping the MIP Web interface
  ```
  mip stop
  ```
* Restarting the MIP Web interface
  ```
  mip restart
  ```
  Note that a *restart* is actually different from a "*stop* *start*" cycle. See the Docker documentation.

At anytime, you can learn more about the *mip* commands with:
```
mip --help
```
