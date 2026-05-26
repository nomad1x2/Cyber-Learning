# Interface Configuration

## Overview

Linux interface configuration varies by distro/renderer. Using `/etc/network/interfaces` (Kali), `netplan` (Ubuntu), and `nmcli` (NetworkManager)
Always check interface names with `ip a` before editing any config file

---

## /etc/network/interfaces — Kali

Used on Kali, edit directly to set static IPs

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

| Command | Description |
|---------|-------------|
| `ip a` | Show current interface names and addresses |
| `sudo vim /etc/network/interfaces` | Edit static interface config |
| `sudo systemctl restart networking` | Apply changes |

---

## netplan — Ubuntu

Used on Ubuntu. Config lives in `/etc/netplan/`. File must be valid YAML, similar to python, whitespace matters

```bash
sudo vim /etc/netplan/02-interfaces.yaml
```

```yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    ens33:
      dhcp4: false
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
      addresses:
        - 2.2.2.30/24
```

```bash
# Apply and verify
sudo netplan apply
ping 192.168.8.200
```

If the interface doesn't come up with netplan, bring it up manually with nmcli:

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses 2.2.2.30/24 ipv4.method manual
sudo nmcli con up "Wired connection 1"
```

| Command | Description |
|---------|-------------|
| `sudo netplan apply` | Apply netplan config |
| `sudo nmcli con mod` | Modify a connection's settings |
| `sudo nmcli con up` | Bring a connection up |

---

## nmcli — Debian

Used on Debian with NetworkManager. No config file to edit, just using CLI

```bash
# Check existing connections
nmcli con show

# Configure both interfaces
sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.8.203/24 ipv4.gateway 192.168.8.1 ipv4.dns 192.168.8.1 ipv4.method manual
sudo nmcli con mod "ens37" ipv4.addresses 2.2.2.40/24 ipv4.method manual

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

## Screenshots

---

## Notes / Gotchas

- Interface names (`eth0`, `ens33`, etc.) aren't the same on every machine, always run `ip a` first
- Netplan is strict about YAML whitespace
- If netplan renderer is `NetworkManager`, nmcli and netplan could conflict
- `/etc/network/interfaces` and netplan should not both be managing the same interface