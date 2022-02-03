[Federated MIP Deployment](Readme.md#PreparingMaster) -> `Preparing the master node`

# Preparing the **master** node
1. Install the **master**

   As a "sudoer" user:
   1. Set the hostname, with a meaningful name, i.e.
      ```
      sudo hostnamectl set-hostname <FEDERATION_NAME>-ms
      ```
   1. Configure the networking, including the DNS client
   1. Install the MIP
      ```
      git clone https://github.com/HBPMedical/mip-deployment
      ```
      ```
      sudo mip-deployment/mip --node-type ms --yes install
      ```
      Here, the *--node-type* parameter is very important, because it tells the script that this node will be a **master** (ms).  
      Following the same process than for the workers, you can also put the specific parameters (*--version*, *--branch* or *--commit*, used with the flag *--force-install-unstable*) if you want to install a specific version.

1. Configure the **master**

   Still as a "sudoer" user:
   ```
   sudo mip --node-type ms --yes configure all
   ```

   Like for the workers, by default, this will create a user *mipadmin*, and you can also change its password:
   ```
   sudo passwd mipadmin
   ```

   Again, later on, you will have to give the *pusher* informations about this *master* node:
   * Its IP address
   * The user (*mipadmin*)
   * The user's password

1. Prepare the CDE metadata files (**only if you don't want to automatically download their latest version on the data catalogue**)

   If you want to manage your CDEs by yourself, you'll have to place them on the **master** node, as follows.  
   * For every pathology over the whole federation, as **mipadmin** user:
     ```
     sudo mkdir -p /data/<FEDERATION_NAME>/<PATHOLOGY_NAME>
     ```
   * Then, still as **mipadmin**, place the corresponding *CDEsMetadata.json* file in the right pathology folder.
   * Once it's done, you can set the data owner to *mipadmin*
     ```
     sudo chown -R mipadmin.mipadmin /data
     ```
