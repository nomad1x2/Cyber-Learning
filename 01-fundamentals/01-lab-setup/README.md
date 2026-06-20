
# Lab Setup
 
VM-based lab and setup notes:
 
---
 
## Network Config
 
| Machine | Username | 							IPs	 			    |      Tunnel      | 
|---------|----------|------------------------------|------------------| 
| Kali    | nomad    | 192.168.8.200 / 1.1.1.10 | wireguard - 172.16.10.2 |
| Debian  | User01   | 192.168.8.203 / 2.2.2.40 | openvpn - 172.16.20.1   |
| Ubuntu  | User02   | 192.168.8.202 / 2.2.2.30 / 172.16.0.1 | wireguard - 172.16.10.1 |
| Windows | User03   | 192.168.8.201 / 1.1.1.20 | openvpn - 172.16.20.x/24  |
| Pi Zero W | pi   | 192.168.8.50 |  (ProxyJump to target net / ubuntu pivot)
| Windows XP | Target01   | 172.16.0.27 |  N/A   |
| Metasploitable | Target02   | 172.16.0.50 |  N/A   |
| Windows 7 | Target03   | 172.16.0.150 |  N/A   |
 
---
 
## Network Topology
 
![net-topo](../../assets/images/net-topology.png)
 
---
 
## Environment
 
- Laptop 1: Hypervisor hosting Windows 11 + Kali Linux VMs (WiFi)
- Laptop 2: Hypervisor hosting Debian + Ubuntu (Ethernet)
  - Plus target machines (Metasploitable, Windows 7, Windows XP)
- Pi Zero W: 2.4ghz WiFi
- Router: GLiNet wireless, tethered internet

| Network| Network    | 
|--------|-----------------------| 
| GLiNet | 192.168.8.0 /24|
| VMnet1 | 1.1.1.0 /24    |
| VMnet2 | 2.2.2.0 /24|
| VMnet3 | 172.16.0.0 /24|

- Hypervisor: VMware
---

## Raspberry Pi Zero W (1)

Running the `2026-04-21-raspios-trixie-armhf-lite` image

Add route to reach Target nets through Ubuntu (not persistent):
- `sudo route add -net 172.16.0.0 netmask 255.255.255.0 gw 192.168.8.202`

---

## Debian
 
Had to add user to sudo group after install:
 
```bash
su -
sudo usermod -aG sudo nomad
# refresh group - takes effect in new session
```

---
 
## Windows 11
 
Fresh install required bypassing the network/Microsoft account requirement:
 
```
SHIFT+F10 -> OOBE\BYPASSNRO
```
 
Ref:
- https://dev.to/alanwest/how-to-set-up-windows-11-without-a-microsoft-account-2026-edition-4c7a
 
---

## Metasploitable
 
Network config:
 
```bash
sudo gedit /etc/network/interfaces

auto eth0
iface eth0 inet static
address 172.16.0.50
network 255.255.255.0
```

---

## Known Issues
 
- Laptop 1 physical bridge instability on wired Ethernet - switched to WiFi bridge
- Kali VM: mouse input issue resolved by upgrading VM hardware compatibility to 17.5+
- Windows 11 firewall blocked ping by default (ICMP disabled inbound)
  - Also, install `VMWare Tools`
- Debian install did not add default user to sudoers
- Had to add default route in metasploitable
  - `route add default gw 172.16.0.1`