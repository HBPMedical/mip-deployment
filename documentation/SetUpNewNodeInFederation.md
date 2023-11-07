# Configuring a New Node in the Federation

To add a new node to the federation, you need to follow these steps, which involve creating a mipadmin user, configuring VPN settings, and performing several other tasks to ensure seamless integration. Here's a more detailed and organized guide:

## VPN VM Configuration Steps:

Before configuring the new node, make sure you complete the following steps on the VPN VM:

1. Access the VPN VM: Connect to the VPN VM using the following command:

   ```bash
   ssh -J mipadmin@mipintns1.hbpmip.link mipadmin@vpn1.mip
   ```

2. Configure VPN Federation Hub: Use the following command to configure VPN settings:

   ```bash
   sudo /opt/softether-vpn/vpncmd/vpncmd
   ```

   You need to configure the hub of the federation you are intending to add a new node. You will need to create a user and assign a password.

3. Access Federation Client Folder: Navigate to the folder containing client configurations for the federation where you intend to add the new client:

   ```bash
   cd /home/mipadmin/openvpn/clients/<federation>/
   ```

4. Create a New Client Configuration File: Create a new configuration file for the new node, using a name like 'wkferes'. The file should include the following information:

   ```bash
   VPN_CIDR_ADDRESS=10.86.X.Y/24
   VPN_CIDR_ROUTE=10.86.20.0/24
   VPN_GATEWAY=10.86.X.1
   ```

   Replace 'X' with the federation-specific number and 'Y' with a unique node number within the federation, which should not already exist.

## Node Configuration Steps:

1. Create mipadmin User:
   - Access the VM with administrative privileges using `sudo -i`.
   - Update the package list with `apt-get update`.
   - Upgrade system packages with `apt-get dist-upgrade -u`.
   - Reboot the VM.
   - Create the mipadmin user with `adduser mipadmin`.
   - Grant sudo privileges to mipadmin with `adduser mipadmin sudo`.
   - Switch to the mipadmin user with `su mipadmin`.

2. Allow Access to mipintns1:
   - Ensure that the mipadmin user can be accessed by mipintns1.
   - Create an SSH directory if it doesn't exist with `mkdir .ssh`.
   - Navigate to the .ssh directory with `cd .ssh`.
   - Copy the authorized keys from mipintns1 with `scp mipintns1.hbp.link:/opt/ssh_access/authorized_keys`.
   - Navigate back to the home directory with `cd ....`

3. Update resolve.conf for Federation:
   - Modify `resolved.conf` with `sudo nano /etc/systemd/resolved.conf`.
   - In the `[Resolve]` section, change `#DNS` to `DNS=10.86.20.2`.
   - Set `#Domains` to `Domains=<federation>.mip` (e.g., `Domains=stroke.mip`).
   - Restart the systemd-resolved service with `sudo systemctl restart systemd-resolved.service`.

4. Set Hostname:
   - Update the VM hostname to a relevant name with `sudo hostnamectl set-hostname <hostname>` (e.g., `sudo hostnamectl set-hostname wkbasel`).
   - Reboot the VM with `sudo reboot`.

5. Configure OpenVPN:
   - Copy the OpenVPN configuration script with `scp -J mipadmin@mipintns1.hbp.link mipadmin@vpn1.mip:openvpn/openvpn_setup.sh`.
   - Execute the configuration script with `sudo ./openvpn_setup.sh`. Additional documentation may be required for this script.

6. Verify OpenVPN Configuration:
   Confirm that the OpenVPN configuration is correct by:
   - Running `ifconfig`.
   - Checking for the virtual adapter for the VPN, typically named `tap1` or `vpn_hbp`. It should have information about `inet`. If not, add it with `sudo ip address add 10.86.<specific for each fed>.<new no existing ip for the node>/24 dev vpn_hbp/tap1` (e.g., `sudo ip address add 10.86.102.13/24 dev vpn_hbp`).
   - Adding a route with `sudo ip route add 10.86.20.0/24 via 10.86.<specific for each fed>.1 dev vpn_hbp/tap1` (e.g., `sudo ip route add 10.86.20.0/24 via 10.86.102.1 dev vpn_hbp`).

7. Verify Configuration Files:
   Ensure the following configuration files are correctly set:
   - `/etc/openvpn/client/vpn.hbp.link.conf`
   - `/etc/openvpn/client/vpn.hbp.link.creds`
   - `/etc/netplan/02-vpn.hbp.link.yaml`
   - `/etc/networkd-dispatcher/configured.d/10-vpn.hbp.link`
   - `/etc/networkd-dispatcher/routable.d/10-vpn.hbp.link-routable`

By following these steps, you should successfully set up a new node in the federation. Ensure that all configurations are accurate to avoid any issues in your federated environment.