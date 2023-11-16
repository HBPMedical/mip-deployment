# Configuring a New Node in the Federation

Integrating a new node into your federation involves several critical steps. These steps encompass the creation of a mipadmin user, configuring VPN settings, and other essential tasks to ensure smooth integration into the federation network.

## VPN VM Configuration Steps

Prior to configuring the new node, complete the following preliminary steps on the VPN VM:

1. **Access the VPN VM**
   Connect to the VPN VM using SSH:
   ```bash
   ssh mipadmin@vpn.hbp.link
   ```

2. **Configure VPN Federation Hub**
   Enter the VPN command line interface to configure the VPN settings specific to your federation:
   ```bash
   sudo /opt/softether-vpn/vpncmd/vpncmd
   ```
   Within this interface, configure the federation's hub. This involves creating a user for the new node and assigning a password.

3. **Access Federation Client Folder**
   Navigate to the directory containing the federation's client configurations:
   ```bash
   cd /home/mipadmin/openvpn/clients/<federation>/
   ```

4. **Create New Client Configuration**
   Generate a configuration file for the new node. Use the VPN user's name for the file name and include network settings:
   ```bash
   VPN_CIDR_ADDRESS=10.86.X.Y/24
   VPN_CIDR_ROUTE=10.86.20.0/24
   VPN_GATEWAY=10.86.X.1
   ```
   Here, replace 'X' with the federation-specific number and 'Y' with a unique node identifier within the federation.

## Node Configuration Steps

1. **Create mipadmin User**
   - Access the VM as a superuser: `sudo -i`.
   - Update and upgrade system packages: `apt-get update && apt-get dist-upgrade -u`.
   - Reboot the VM.
   - Create a new user, mipadmin: `adduser mipadmin`.
   - Grant administrative privileges: `adduser mipadmin sudo`.
   - Switch to mipadmin: `su mipadmin`.

2. **Enable Access for mipintns1**
   - Ensure mipadmin is accessible by mipintns1.
   - Create an SSH directory: `mkdir -p ~/.ssh && cd ~/.ssh`.
   - Import authorized keys from mipintns1: `scp mipadmin@mipintns1.hbp.link:/opt/ssh_access/authorized_keys .`

3. **Configure DNS for Federation**
   - Edit `resolved.conf`: `sudo nano /etc/systemd/resolved.conf`.
   - Under `[Resolve]`, set the DNS and Domains for the federation, e.g., `DNS=10.86.20.2`, `Domains=stroke.mip`.
   - Restart the DNS resolver: `sudo systemctl restart systemd-resolved.service`.

4. **Set Hostname**
   - Update the hostname to reflect its role: `sudo hostnamectl set-hostname <hostname>`, e.g., `sudo hostnamectl set-hostname wkbasel`.
   - Reboot to apply changes.

5. **Configure OpenVPN**
   - Fetch the OpenVPN setup script: `scp mipadmin@vpn.hbp.link:openvpn/openvpn_setup.sh .`
   - Run the configuration script: `sudo ./openvpn_setup.sh`.
   - Refer to [Openvpn Setup Script Documentation](vpn/VPNClientConfiguration.md) for detailed instructions.
