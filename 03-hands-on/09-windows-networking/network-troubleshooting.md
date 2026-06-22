# Basic Network Commands on Windows

## nbtstat

Displays protocol statistics and current TCP/IP connections using NBT (NetBIOS over TCP/IP)

Against a Linux target (Ubuntu):
```cmd
nbtstat -A 192.168.8.202

Local Area Connection:
Node IpAddress: [0.0.0.0] Scope Id: []
    Host not found.
Ethernet0:
Node IpAddress: [192.168.8.201] Scope Id: []
    Host not found.
Ethernet1:
Node IpAddress: [1.1.1.20] Scope Id: []
    Host not found.
```

Against a Windows target (physical hypervisor laptop):
```cmd
nbtstat -A 192.168.8.134

Ethernet0:
Node IpAddress: [192.168.8.201] Scope Id: []
           NetBIOS Remote Machine Name Table
       Name               Type         Status
    ---------------------------------------------
    LAPTOP-7SLS1EV9<00>  UNIQUE      Registered
    LAPTOP-7SLS1EV9<20>  UNIQUE      Registered
    WORKGROUP      <00>  GROUP       Registered
    MAC Address = 4C-ED-FB-D8-4C-DE
```

Type codes:
| Code | Meaning |
|----|----|
| `<00>` UNIQUE | Workstation service name |
| `<20>` UNIQUE | File server service name |
| `<00>` GROUP  | Workgroup or domain name |

NetBIOS is Windows native
- Linux host returns "Host not found" since ubuntu either is not running Sambas nmbd or has NetBIOS disabled
- Windows host responds with a full name table

---

## ipconfig

Displays IP configuration for all network adapters:
```cmd
ipconfig /all

Unknown adapter Local Area Connection:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : TAP-Windows Adapter V9 for OpenVPN Connect
   Physical Address. . . . . . . . . : 00-FF-08-D9-27-A5
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::ee54:2262:a256:f4b9%4(Preferred)
   IPv4 Address. . . . . . . . . . . : 172.16.20.2(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . :
   DHCPv6 IAID . . . . . . . . . . . : 369164040
   DHCPv6 Client DUID. . . . . . . . : 00-01-01-00-31-A2-AC-EA-00-0C-29-C8-7A-72
   DNS Servers . . . . . . . . . . . : 10.129.14.201
   NetBIOS over Tcpip. . . . . . . . : Enabled
   
Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Intel(R) 82574L Gigabit Network Connection
   Physical Address. . . . . . . . . : 00-0C-29-C8-7A-72
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   IPv6 Address. . . . . . . . . . . : fd00::201(Preferred)
   Link-local IPv6 Address . . . . . : fe80::aaa:1f68:e09e:1c84%13(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.8.201(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.8.1
   DHCPv6 IAID . . . . . . . . . . . : 184552489
   DHCPv6 Client DUID. . . . . . . . : 00-01-01-00-31-A2-AC-EA-00-0C-29-C8-7A-72
   DNS Servers . . . . . . . . . . . : 192.168.8.1
   NetBIOS over Tcpip. . . . . . . . : Enabled

Ethernet adapter Ethernet1:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Intel(R) 82574L Gigabit Network Connection #2
   Physical Address. . . . . . . . . : 00-0C-29-C8-7A-7C
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::2a0e:cfcb:98a4:fb5f%17(Preferred)
   IPv4 Address. . . . . . . . . . . : 1.1.1.20(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . :
   DHCPv6 IAID . . . . . . . . . . . : 301993001
   DHCPv6 Client DUID. . . . . . . . : 00-01-01-00-31-A2-AC-EA-00-0C-29-C8-7A-72
   DNS Servers . . . . . . . . . . . : 10.129.14.201
   NetBIOS over Tcpip. . . . . . . . : Enabled

Unknown adapter OpenVPN Connect DCO Adapter:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : OpenVPN Data Channel Offload
   Physical Address. . . . . . . . . :
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
```

Plain `ipconfig` without flags shows only basic info
- `/all` shows additional details per adapter like DNS/DHCP servers

---

## getmac

Lists the MAC address and network device path for each adapter:
```cmd
getmac

Physical Address    Transport Name
=================== ==========================================================
00-0C-29-C8-7A-72   \Device\Tcpip_{BC5E5F9F-CCD7-4576-A175-BF733994D95C}
00-0C-29-C8-7A-7C   \Device\Tcpip_{FC673DF4-51F3-4D7B-91DC-FBA47EA21F7E}
00-FF-08-D9-27-A5   \Device\Tcpip_{08D927A5-A690-414B-8FB8-5242BE9AF23E}
N/A                 Media disconnected
```

Adapters showing "Media disconnected" have no active link, that OpenVPN TAP adapter is not currently in use

---

## tracert

Maps the path packets take to reach a destination:
```cmd
tracert 8.8.8.8

Tracing route to dns.google [8.8.8.8]
over a maximum of 30 hops:
  1     3 ms     2 ms     2 ms  console.gl-inet.com [192.168.8.1]
  2    51 ms    48 ms    48 ms  10.2.0.1
  3     *        *        *     Request timed out.
  4    55 ms    93 ms    49 ms  ae0-3101.bb1.lax1.us.m247.ro [83.97.21.118]
  5    55 ms    50 ms    50 ms  146.70.4.244
  6    61 ms     *       53 ms  146.70.195.186
  7    51 ms    49 ms    53 ms  142.251.254.245
  8    49 ms    48 ms    49 ms  142.251.233.237
  9    52 ms    51 ms    57 ms  dns.google [8.8.8.8]
Trace complete.
```

- Hop 1 is the GLiNet router (our gateway)
- Hop 2 is an external WireGuard peer (10.2.0.1) configured on the GliNet router
- Hop 3 shows "Request timed out", that hop is dropping ICMP but the trace continues past it since later hops still respond
- Hops 4 through 9 route thru the ISP backbone before reaching a google DNS server (8.8.8.8)

---

## Notes / Gotchas

- A single-hop `tracert` result confirms the destination is on the same broadcast domain, more hops would appear if routing through a gateway