# Interface Configuration

## Overview

Windows interface configuration can be done via the GUI (ncpa.cpl) or PowerShell
Always verify adapter names with `Get-NetAdapter` before running PowerShell commands

---

## GUI - Ethernet0 (GLiNet)

Go to the adapter settings and set static values:

```
ncpa.cpl -> Double click Ethernet0 -> Properties -> IPv4
```

```
IP Address:  192.168.8.201
Subnet Mask: 255.255.255.0
Gateway:     192.168.8.1
DNS:         192.168.8.1
```

---

## PowerShell - Ethernet1 (vmnet1)

```powershell
# List adapters to verify correct names
Get-NetAdapter

# Assign static IP to the VMnet1 adapter
New-NetIPAddress -InterfaceAlias "Ethernet1" -IPAddress 1.1.1.20 -PrefixLength 24

# Add a persistent route to reach vmnet2 through the OpenVPN tunnel
route -p add 2.2.2.0 mask 255.255.255.0 10.2.0.1

# Verify
ipconfig
route print
ping 192.168.8.1
ping 1.1.1.10
```

| Command | Description |
|---------|-------------|
| `Get-NetAdapter` | List all adapters and their current state |
| `New-NetIPAddress` | Assign a static IP to a named adapter |
| `route -p add` | Add a persistent static route that survives reboot |
| `ipconfig` | Verify IP assignments on all interfaces |
| `route print` | Verify the full routing table |

---

## Screenshots

---

## Notes / Gotchas

- Adapter names in PowerShell must match exactly, use `Get-NetAdapter` first to confirm
- `-p` flag on `route add` makes the route persistent across reboots
- If `New-NetIPAddress` throws a conflict error, remove the existing address first with `Remove-NetIPAddress`