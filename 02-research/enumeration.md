# Enumeration

Actively scanning a target to extract detailed information
- Identify users, shares, services, OS versions, open ports, vulnerabilities, etc.
- Different than standard recon as you are _actively_ touching the target rather than passive information gathering

| Type | What you're looking for |
|------|------------------------|
| Network enumeration | Open ports, services, OS fingerprinting |
| User enumeration | Valid usernames, groups, password policies |
| Share enumeration | SMB shares, NFS mounts, accessible files |
| Service enumeration | Software versions, misconfigurations |

Once you can gather enough information on a targets' open ports and what not, you can then research deeper and look for any potential vulnerabilities

---

## nmap

**Network Mapper** - network scanning tool
- Maps open ports, identifies services, fingerprints OS
- Can run scripts (NSE) to go deeper into vulnerabilities

| Flag | What it does |
|------|-------------|
| `-sS` | SYN scan (stealth) - half-open, doesn't complete TCP handshake |
| `-sV` | Version detection - identifies service versions |
| `-O` | OS fingerprinting (not always accurate) |
| `-pX,Y-Z` | Scan selected ports |
| `-p-` | Scan all 65535 ports |
| `-A` | Aggressive scan - OS, version, scripts, traceroute |
| `-sU` | UDP scan |
| `-sT` | TCP scan |
| `-sn` | Ping sweep - host discovery, no port scan |
| `-Pn` | Treat host as up - skip host discovery |
| `-sC` | Script scan - default NSE scripts |
| `--script` | Run NSE scripts (vuln, auth, brute, etc) |
| `-oA / -oN / -oX / -oG` | Output to all / normal / XML file / greppable |

```bash
#Service version/os/syn scan/all ports
nmap -sS -sV -O -p- 192.168.8.200

#Service version/os/syn scan/selected ports
nmap -sS -sV -O -p22,445-8080 192.168.8.200

#Aggressive scan and vuln scripts, subnet
nmap -A --script=vuln 192.168.8.0/24
```

Ref:
- https://nmap.org/

---

## enum4linux

Tool for enumerating **SMB/Samba** info from Windows and Linux boxes
- Wrapper around `smbclient`, `rpcclient`, `net`, and `nmblookup`
- Pull users, groups, shares, password policies

| Flag | What it does |
|------|-------------|
| `-a` | All simple enumeration |
| `-U` | Get userlist |
| `-M` | Get machine list |
| `-S` | Get sharelist |
| `-P` | Get password policy information |
| `-G` | Get group and member list |
| `-u` | Specify username to use (default: `""`) |
| `-p` | Specify password to use (default: `""`) |

```bash
#All simple:
enum4linux -a 172.16.0.50
...
[+] Got OS info for 172.16.0.50 from srvinfo: 
	METASPLOITABLE Wk Sv PrQ Unx NT SNT metasploitable server (Samba 3.0.20-Debian)
	platform_id     :	500
	os version      :	4.9
	server type     :	0x9a03

...

#User enumeration
enum4linux -U 172.16.0.150
...
 ========================================( Users on 172.16.0.50 )========================================

index: 0x1 RID: 0x3f2 acb: 0x00000011 Account: games	Name: games	Desc: (null)
index: 0x2 RID: 0x1f5 acb: 0x00000011 Account: nobody	Name: nobody	Desc: (null)
index: 0x3 RID: 0x4ba acb: 0x00000011 Account: bind	Name: (null)	Desc: (null)
index: 0x4 RID: 0x402 acb: 0x00000011 Account: proxy	Name: proxy	Desc: (null)
index: 0x5 RID: 0x4b4 acb: 0x00000011 Account: syslog	Name: (null)	Desc: (null)
index: 0x6 RID: 0xbba acb: 0x00000010 Account: user	Name: just a user,111,,	Desc: (null)
index: 0x7 RID: 0x42a acb: 0x00000011 Account: www-data	Name: www-data	Desc: (null)
index: 0x8 RID: 0x3e8 acb: 0x00000010 Account: root	Name: root	Desc: (null)
...

#Share enumeration
enum4linux -S 192.168.8.202

 =================================( Share Enumeration on 192.168.8.202 )=================================

smbXcli_negprot_smb1_done: No compatible protocol selected by server.

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	RemoteShare     Disk      
	IPC$            IPC       IPC Service (ubuntu server (Samba, Ubuntu))

```

Ref:
- https://www.kali.org/tools/enum4linux/

---

## WindowsEnum

PowerShell script for local enumeration on a Windows host
- Run after you have a foothold 
- Privilege escalation prep

| What it pulls | Details |
|--------------|---------|
| System info | OS version, hostname, patch level |
| Local users / groups | Who's on the box, who's an admin, etc |
| Running processes | Whats actively running |
| Scheduled tasks | Potential persistence or privesc paths |
| Network info | Interfaces, routes, connections |
| Installed software | Versions that may be vulnerable |

```powershell
PS C:\Users\User03\Desktop> powershell -nologo -executionpolicy bypass -file WindowsEnum.ps1

------------------------------------------
  Windows Enumeration Script v 0.1
          by absolomb
       www.sploitspren.com
------------------------------------------

------------------------------------------
  Basic System Information
------------------------------------------

Host Name:                     DESKTOP-R4EM499
OS Name:                       Microsoft Windows 11 Home
OS Version:                    10.0.26200 N/A Build 26200
OS Manufacturer:               Microsoft Corporation
OS Configuration:              Standalone Workstation
OS Build Type:                 Multiprocessor Free
Registered Owner:              User03
Registered Organization:       N/A
Product ID:                    00326-30000-00001-AA306
Original Install Date:         5/22/2026, 5:04:59 PM
System Boot Time:              6/20/2026, 7:15:59 PM
System Manufacturer:           VMware, Inc.
System Model:                  VMware20,1
System Type:                   x64-based PC
Processor(s):                  1 Processor(s) Installed.
                               [01]: Intel64 Family 6 Model 170 Stepping 4 GenuineIntel ~3072 Mhz
BIOS Version:                  VMware, Inc. VMW201.00V.24006586.B64.2406042154, 6/4/2024
Windows Directory:             C:\WINDOWS
System Directory:              C:\WINDOWS\system32
Boot Device:                   \Device\HarddiskVolume1
...
```

Ref:
- https://github.com/absolomb/WindowsEnum/tree/master

## Notes

- I had some problems running this on Win7, potentially version mismatch?
  - Flawless execution on my Win11 platform; gave all the deets

---

## JAWS
- Just Another Windows Script - PowerShell post-exploitation enumeration
- Similar to WindowsEnum but focused on privesc
- Outputs a checklist of potential weaknesses
  - Unquoted service paths, AlwaysInstallElevated, weak service permissions, stored creds

| What it checks | Details |
|-------|---------|
| Running Processes | Find privileged targets |
| Writable Files Folders | Replace binaries DLL hijack |
| Vulnerable Services | Service abuse |
| Unquoted Service Paths | Service hijack |
| Stored Credentials | Recover passwords |
| Scheduled Tasks | Task hijack |
| AlwaysInstallElevated | MSI as SYSTEM |
| Installed Applications | Known exploits |
| Writable PATH | Binary planting |
| Network Information | Pivoting |
| Firewall Rules | Find exposed services |

```powershell
<#Output to screen#>
powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1

<#Output to file#>
powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1 -OutputFilename JAWS-Enum.txt
```

After gaining access into a Win7 box:
```powershell
C:\Windows\TEMP>powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1
powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1

Running J.A.W.S. Enumeration
	- Gathering User Information
	- Gathering Processes, Services and Scheduled Tasks
	- Gathering Installed Software
	- Gathering File System Information

	- Looking for Simple Priv Esc Methods
############################################################
##     J.A.W.S. (Just Another Windows Enum Script)        ##
##                                                        ##
##           https://github.com/411Hall/JAWS              ##
##                                                        ##
############################################################

Windows Version: Microsoft Windows 7 Home Premium 
Architecture: AMD64
Hostname: TARGET03-PC
Current User: TARGET03-PC$
Current Time\Date: 07/02/2026 18:14:50

-----------------------------------------------------------
 Users
-----------------------------------------------------------
----------
Username: Administrator
Groups:   Administrators
----------
Username: Guest
Groups:   Guests
----------
Username: Target03
Groups:   Administrators
...
```
Ref:
- https://github.com/411Hall/JAWS/tree/master

---

# RID Cycling

- RID = number tied to every Windows account
  - Relative Identifiers (RIDs)
- Cycling = brute forcing those numbers to find accounts

Ref:
- https://rioasmara.com/2026/01/11/the-silent-kill-chain-from-rid-cycling-to-ad-cs-template-injection/