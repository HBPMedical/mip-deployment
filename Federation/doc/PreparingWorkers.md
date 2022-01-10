<a href="Readme.md#PreparingWorkers">Federated MIP Deployment</a> -> `Preparing the worker nodes`

# Preparing the **worker** nodes
1. Install the **workers**

   On each worker node, as a "sudoer" user:
   1. Set the hostname, with a meaningful name, i.e.
      ```
      sudo hostnamectl set-hostname <FEDERATION_NAME>-wk<WORKER_NUMBER>
      ```
   1. Configure the networking, including the DNS client
   1. Install the MIP
      ```
      git clone https://github.com/HBPMedical/mip-deployment
      ```
      ```
      sudo mip-deployment/mip --node-type wk --yes install
      ```
      Here, the *--node-type* parameter is very important, because it tells the script that this node will be a **worker** (wk).  
      If you want to install a specific version of the MIP, you can precise the tag (*--version \<TAG>*), the branch (*--branch \<BRANCH>*) or even the commit ID (*--commit \<COMMIT>*), each of these parameters having precedence over the next one(s). If you specify a non-default version, you also have to force this installation with the flag *--force-install-unstable*.

      Don't hesitate to use:
      ```
      mip --help
      ```

1. Configure the **workers**

   On each worker node, still as a "sudoer" user:
   ```
   sudo mip --node-type wk --yes configure all
   ```

   By default, this will create a user *mipadmin* (which will be in *docker* and *sudo* groups). This user will be used by the *pusher* to operate this node. If you don't know its password or want to change it, do it right now with:
   ```
   sudo passwd mipadmin
   ```

   Later on, you (or the central system administrator) will need to provide the *pusher* node informations about this *worker* node:

   * The node IP address, with which the pusher will connect (via ssh), using the *mipadmin* user:
     ```
     ip a
     ```
     This command will give you the machine's networking configuration details. You'll have to search for the IP with which you will reach this node from the other federation's nodes. If you prepared a VPN network, you'll have to use the VPN IP of this node.
   * The user (*mipadmin*)
   * The user's password

1. Prepare the datasets on the **workers**

   * On each worker, as **mipadmin** (*sudo su - mipadmin* can help you becoming this user if you don't know its password) user, prepare the federation data folder. Go with this pattern:
     ```
     sudo mkdir -p /data/<FEDERATION_NAME>
     ```

     If your federation is named *mipfed1*, the data folder will have to be */data/mipfed1*.  
   * Place your datasets in /data/<FEDERATION_NAME>/<PATHOLOGY_NAME>/
   * If you have CDE metadata files, it will have to be, or placed in the **master** node, or downloaded (latest version for now) from the central data catalogue.
   * Set the data folder to be owned by *mipadmin*
     ```
     sudo chown -R mipadmin.mipadmin /data
     ```
