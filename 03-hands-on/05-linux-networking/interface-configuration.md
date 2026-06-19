

# Interface Configuration

## Overview

Linux interface configuration varies by distro/renderer. This lab uses `/etc/network/interfaces` on Kali, `netplan` on Ubuntu, and `nmcli` with NetworkManager on Debian

Always check interface names with `ip a` before editing any config file

---

## /etc/network/interfaces - Kali

Edit `/etc/network/interfaces` directly to configure static IP addresses

```bash
sudo vim /etc/network/interfaces
```

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 192.168.8.200
    netmask 255.255.255.0
    gateway 192.168.8.1
    dns-nameservers 192.168.8.1

auto eth1
iface eth1 inet static
    address 1.1.1.10
    netmask 255.255.255.0
```

```bash
# Apply and verify
sudo systemctl restart networking
ping 192.168.8.1
```

### IPv6 (Added post IPv4 config)
Add to `/etc/network/interfaces` under the eth0 block:
```
iface eth0 inet6 static
    address fd00::200
    netmask 64
```
```bash
sudo ifdown eth0 && sudo ifup eth0
# ipv6 address not found during ifdown since none was configured previously

ip -6 addr show eth0
# inet6 fd00::200/64 scope global
```

![ipv6 kali](../../assets/images/linux/ipv6kali.png)

| Command | Description |
|---------|-------------|
| `ip a` | Show current interface names and addresses |
| `sudo vim /etc/network/interfaces` | Edit static interface config |
| `sudo systemctl restart networking` | Apply changes |

---

## netplan - Ubuntu

Used on Ubuntu. Config lives in `/etc/netplan/`. File must be valid YAML, similar to python, whitespace matters
- Edited the original netplan: included new network for metasploitable

```bash
sudo vim /etc/netplan/02-interfaces.yaml
```

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
  
    ens33:
      dhcp4: false
      dhcp6: false
      addresses:
        - 192.168.8.202/24
      routes:
        - to: default
          via: 192.168.8.1
      nameservers:
        addresses:
          - 192.168.8.1
          
    ens37:
      dhcp4: false
      dhcp6: false
      addresses:
        - 2.2.2.30/24
        
    ens38:
      dhcp4: false
      dhcp6: false
      addresses:
        - 172.16.0.1/24
```

```bash
# Fix permissions then apply and verify
sudo chmod 600 /etc/netplan/02-interfaces.yaml
sudo netplan apply
ping 192.168.8.200

User02@ubuntu:/etc/netplan$ networkctl list
IDX LINK  TYPE      OPERATIONAL SETUP     
  1 lo    loopback  carrier     unmanaged
  2 ens33 ether     routable    configured
  3 ens37 ether     routable    configured
  4 ens38 ether     routable    configured
  5 wg0   wireguard routable    unmanaged

5 links listed.
```

### IPv6 (Added post IPv4 config)

Add ipv6 address directly to the yaml under ens33:

```bash
sudo vim /etc/netplan/02-interfaces.yaml
```

```yaml
    ens33:
      dhcp4: false
      dhcp6: false
      addresses:
        - 192.168.8.202/24
        - fd00::202/64
```

```bash
sudo netplan apply

User02@ubuntu:/etc/netplan$ ip -6 addr show ens33
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp2s1
    altname enx000c295864fb
    inet6 fd00::202/64 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe58:64fb/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```

![ipv6 ubuntu](../../assets/images/linux/ipv6ubuntu.png)

| Command | Description |
|---------|-------------|
| `sudo netplan apply` | Apply netplan config |
| `networkctl list` | Show all interfaces and their state |
| `networkctl status <iface>`  | Detailed status for a specific interface |

---

## nmcli - Debian

Used on Debian with NetworkManager. NetworkManager stores the connection profiles, so configuration can be done through nmcli:

```bash
# Grab NIC MAC addresses to persist static configs
ip a 
ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether "00:0c:29:96:31:6f" brd ff:ff:ff:ff:ff:ff
ens37: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether "00:0c:29:96:31:79" brd ff:ff:ff:ff:ff:ff
    
# Check existing connections
nmcli con show
    
# Configure both interfaces (also with static MAC)
sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.8.203/24 ipv4.gateway 192.168.8.1 ipv4.dns 192.168.8.1 ipv4.method manual connection.interface-name ens33 802-3-ethernet.mac-address 00:0C:29:96:31:6F
    
sudo nmcli con mod "ens37" ipv4.addresses 2.2.2.40/24 ipv4.method manual connection.interface-name ens37 802-3-ethernet.mac-address 00:0C:29:96:31:79

# Bring them up
sudo nmcli con up "Wired connection 1"
sudo nmcli con up "ens37"

# Verify
ping 192.168.8.202
```

| Command | Description |
|---------|-------------|
| `nmcli con show` | List all connections and their states |
| `nmcli con mod` | Modify a connection property |
| `nmcli con up` | Activate a connection |

---

## IPv6 Connectivity Test
```bash
# Ping between VMs (from kali to Ubuntu and win11)
ping -6 fd00::202
ping -6 fd00::201

# SSH over IPv6
ssh -6 User02@fd00::202
```

![ipv6 ssh](../../assets/images/linux/ipv6ssh.png)

---

## Notes / Gotchas

- Interface names (`eth0`, `ens33`, etc) aren't the same on every machine; always run `ip a` first
- Netplan is strict about YAML whitespace
- Ubuntu vm uses `renderer: networkd`, edit the yaml and run `sudo netplan apply` for any changes
- Netplan will warn about file permissions if the yaml is too open
  - fixed with `sudo chmod 600 /etc/netplan/*.yaml`
- `ens38` added for isolated metasploitable network (`172.16.0.0/24`)
  - requires a third NIC in VMware attached to a separate vmnet
- Debian had some issues keeping interface configs after reboot; pinned to MAC address to fix
- Debian keyboard input lag in VM; fixed by adding `keyboard.vusb.enable = "TRUE"` to the VM's `.vmx` file
  - Ref: https://community.broadcom.com/vmware-cloud-foundation/discussion/ws-1761-keyboard-lag-with-ubuntu-guest
