# Interface Configuration

## Kali VM – Interface Configuration

Using `/etc/network/interfaces` to configure two static interfaces:

### Steps

- Check interface names with `ip a` before making changes, get eth names
- Edit `/etc/network/interfaces`:
  - `eth0` - to GLiNet router (192.168.8.0/24)
  - `eth1` - to vmnet1 internal network (1.1.1.0/24)

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

- Apply and verify:

```bash
sudo systemctl restart networking
ping 192.168.8.1 (gateway)
```

### Commands ran:
`ip a` - show interface config  
`sudo vim /etc/network/interfaces` - edit static config  
`sudo systemctl restart networking` - apply changes  
`ping 192.168.8.1` - verify connectivity  

---

## Ubuntu VM – Interface Configuration

Using netplan to configure two static interfaces:

### Steps

- Check interface names with `ip a`
- Edit `/etc/netplan/02-interfaces.yaml`:
  - `ens33` - to GLiNet router (192.168.8.0/24)
  - `ens37` - to vmnet2 internal network (2.2.2.0/24)

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

- Apply and verify:

```bash
sudo netplan apply
ping 192.168.8.200 (kali vm)
```

- Use NetworkManaget (nmcli) to bring up ens37:

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses 2.2.2.30/24 ipv4.method manual
sudo nmcli con up "Wired connection 1"
```

### Commands ran:
`ip a` - show interface config  
`sudo netplan apply` - apply netplan config  
`sudo nmcli con mod / con up` - configure and bring up ens37

---

## Debian VM – Interface Configuration

Using nmcli to configure two static interfaces:

### Steps

- Check interfaces with `nmcli con show` 
- Configure both interfaces with nmcli:

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.8.203/24 ipv4.gateway 192.168.8.1 ipv4.dns 192.168.8.1 ipv4.method manual
sudo nmcli con mod "ens37" ipv4.addresses 2.2.2.40/24 ipv4.method manual
sudo nmcli con up "Wired connection 1"
sudo nmcli con up "ens37"
```

- Verify:

```bash
ping 192.168.8.202 (ubuntu vm)
```

### Commands ran:
`nmcli con show` - list connections  
`sudo nmcli con mod / con up` - configure static IPs  
