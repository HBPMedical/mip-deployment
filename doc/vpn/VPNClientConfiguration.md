# VPN Client Configuration Guide

## Overview
Our streamlined `openvpn_setup.sh` script is designed to simplify and automate the process of configuring a client machine to connect to a VPN using OpenVPN. This comprehensive script handles various tasks, including package installation, VPN configuration retrieval, credential setup, network configuration with Netplan, and OpenVPN service initiation.

## Accessing the Script

To obtain the `openvpn_setup.sh` script, use the following SCP (Secure Copy Protocol) command:

```bash
scp mipadmin@vpn.hbp.link:openvpn/openvpn_setup.sh .
```

## Prerequisites

Before running the script, ensure the following:

- **Root User**: The script should be executed as the root user for necessary permissions.
- **Software Compatibility**: Ensure OpenVPN and Netplan are compatible with your system.

## Script Details

### Configuration Variables

- `VPN_LINK`: The VPN server's domain or IP address.
- `VPN_CONFIG_FILE`: Path to the OpenVPN configuration file.
- `VPN_CREDS_FILE`: Location of the file storing VPN credentials.
- `VPN_REMOTE_CONFIG_FILE`: Name of the remote OpenVPN configuration file.
- `VPN_SSH_USER`: SSH username for accessing the VPN server.
- `VPN_REMOTE_PATH`: Path on the VPN server for configuration retrieval.
- `VPN_HUB`, `VPN_USER`, `VPN_PASS`: Specific settings for the VPN such as hub name, user, and password.
- `VPN_DEV`, `VPN_CIDR_ADDRESS`, `VPN_CIDR_ROUTE`, `VPN_GATEWAY`: Network interface and routing details for Netplan setup.

### Functional Overview

- `log()`: Function to log messages with timestamp.
- `handle_error()`: Error handling and script termination.
- `install_package()`: Automated installation of required packages using `apt-get`.
- `get_ssh_user()`: Fetches the SSH username for VPN server access.
- `get_vpn_dev()`: Identifies the VPN network device based on the OpenVPN config.
- `get_network_config()`: Interactive setup for VPN network configurations and client-specific settings.

### Initial Operations

- Checks for root privileges.
- Installs `openvpn` and `netplan.io` if not present.

### VPN Configuration Retrieval

- Determines the SSH user.
- Fetches and stores the VPN configuration from the server.

### OpenVPN Credential Setup

- Retrieves network settings.
- Writes VPN credentials to the specified file.

### Netplan Configuration

- Generates a Netplan configuration file with static IP and routing parameters.

### Configuration File Verification

After setup, verify the accuracy of key configuration files:

#### OpenVPN Configuration (`/etc/openvpn/client/vpn.hbp.link.conf`)

- **Purpose**: Stores the VPN's specific settings.
- **Verification**: Ensure alignment with VPN VM settings.

#### OpenVPN Credentials (`/etc/openvpn/client/vpn.hbp.link.creds`)

- **Format**: `node-identifier@hub-name/federation` followed by the password.
- **Example**:
  ```bash
  example_worker@example_federation
  1234
  ```

#### Netplan Configuration (`/etc/netplan/02-vpn.hbp.link.yaml`)

- **Check**: Confirm correct network device, IP address, and routing setup.

### Enabling and Starting OpenVPN Service

- Activates the OpenVPN service with the new configuration.

### Final Confirmation and Activation

- Prompts the user for immediate VPN configuration application. On confirmation, it applies Netplan settings and starts the OpenVPN service.