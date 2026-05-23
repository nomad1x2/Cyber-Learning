## Win11 VM – Interface Configuration

Configuring two interfaces using both the GUI and PowerShell:

### Steps

#### GUI – Ethernet0 (connection to GLiNet)

- Open **ncpa.cpl -> Double click Ethernet0 -> Properties -> IPv4**
- Set static values:

```
IP Address:  192.168.8.201
Subnet Mask: 255.255.255.0
Gateway:     192.168.8.1
DNS:         192.168.8.1
```

#### PowerShell – Ethernet1 (connection to vmnet1)

- List adapters to get/verify the correct names:

```powershell
Get-NetAdapter
```

- Assign static IP to the VMnet1 adapter:

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet1" -IPAddress 1.1.1.20 -PrefixLength 24
```

- Add a persistent route to reach vmnet2 through the OpenVPN tunnel:

```powershell
route -p add 2.2.2.0 mask 255.255.255.0 10.2.0.1
```

- Verify:

```powershell
ipconfig
route print
ping 192.168.8.1
ping 1.1.1.10 (kali vm)
```

### Commands ran:
`Get-NetAdapter` - list adapters  
`New-NetIPAddress` - assign static IP  
`route -p add` - add persistent route  
`ipconfig` - verify IPs  
`route print` - verify routing table 