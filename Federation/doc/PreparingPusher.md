[Federated MIP Deployment](Readme.md#PreparingPusher) -> `Preparing the pusher node`

# Preparing the **pusher** node
As the **pusher** can virtually be any type of node (as it doesn't conflict with any MIP component), the pusher is not a type of node, but a flag in the *mip* script.  
That said, preparing a dedicated **pusher** node is strongly encouraged, in order to avoid any confusion.  
Also, as the **pusher** will operate the federation, remotely controlling the **worker** and the **master** nodes, the federation name will be required for each pusher operation. It also means that a pusher can manage many different federations from the same machine (which can also be a participant node in a federation, at the same time, but again, this kind of setup can become a source of confusions).

1. Install the **pusher**

   As a "sudoer" user:
   1. Set the hostname, with a meaningful name, i.e.
      ```
      sudo hostnamectl set-hostname <FEDERATION_NAME>-pusher
      ```
   1. Configure the networking, including the DNS client
   1. Install the MIP
      ```
      git clone https://github.com/HBPMedical/mip-deployment
      ```
      ```
      sudo mip-deployment/mip --yes --pusher --federation <FEDERATION_NAME> install
      ```
      As said earlier, for the **pusher**, the *--node-type* parameter is not used. Instead, the *--pusher* flag and the *--federation \<FEDERATION_NAME>* parameter are mandatory!  

      In the case of the **pusher**, it's a bit special: as this installation will clone the *exareme* repository, it shouldn't install any version of *exareme*, but instead, it should install the same version which is listed in the *mip-deployment/.versions_env* file, a version which has been tested and validated to work well with the MIP's Web interface.  
      The *exareme* folder will be cloned by default in */opt/\<FEDERATION_NAME>/exareme*, and *mip-deployment* won't be cloned by this installation.  
      That said, some binaries will be cloned from the *mip-deployment* repository, and installed in */usr/local/bin*.

      Following the same process than for the different federation nodes, you can also put the specific parameters (*--version*, *--branch* or *--commit*, used with the flag *--force-install-unstable*) if you want to install a specific version.  
      That said, the specification of the **pusher** makes it a bit trickier, because the along the process, the "signification" of the *--version*, *--branch* or *--commit* parameters can be used to target versions of *exareme*, instead of *mip-deployment*. That's why they should come by pair:

      * *--version \<TAG>* with *--mip-version \<TAG>*
      * *--branch \<BRANCH>* with *--mip-branch \<BRANCH>*
      * *--commit \<COMMIT_ID>* with *--mip-commit \<COMMIT_ID>*

      Again, by default, without specifying anything, the *exareme* version installed will match the one which is written in the *mip-deployment/.versions_env* file of the *mip-deployment* latest stable release, so if you don't understand these complexities, no worries.

      As usual, to get more details, use:
      ```
      mip --help
      ```

1. Configure the **pusher**

   As this operation is something that requires to be interactive at a moment, we won't use *--quiet* nor *--yes* parameters.

   Still as a "sudoer" user:
   ```
   sudo mip --pusher --federation <FEDERATION_NAME> configure all
   ```

   This will first ask you to enter a vault password. This vault will securely store every sensitive details (like credentials) about the remote nodes.  
   For each future tasks which will imply an access on the remote nodes, the *mip* script will ask you this vault password again.  
   Now that this vault question is answered, the *mip configure* process will ask you to provide informations about the **master**, **ui** and **workers** nodes, to prepare SSH identity exchange with the federation participants.  
   For each node (**master**, **ui**, then the **workers**), you'll have to enter:

   * The internal IP address or address which is in the same federation LAN (physical or virtual, if you prepared a VPN).
   * The node's administration user (usually *mipadmin*)
   * This user's password

   The *mip* script will then establish an SSH connection to the node, install its SSH identity there for future passwordless connections, and get the real node's hostname. If you configured the nodes with a meaningful hostname, you should recognize it, and it should actually allow you to verify that you configured the correct machine.
