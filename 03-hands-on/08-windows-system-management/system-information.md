# CLI Detailed system info

---

## CMD (systeminfo)

```cmd
systeminfo

Host Name:                     DESKTOP-R4EM499
OS Name:                       Microsoft Windows 11 Home
OS Version:                    10.0.26200 N/A Build 26200
System Manufacturer:           VMware, Inc.
System Model:                  VMware20,1
Processor(s):                  1 Processor(s) Installed.
                               [01]: Intel64 Family 6 Model 170 Stepping 4 GenuineIntel ~3072 Mhz
Total Physical Memory:         8,191 MB
Available Physical Memory:     4,855 MB
Domain:                        WORKGROUP
Hotfix(s):                     4 Hotfix(s) Installed.
                               [01]: KB5087051
Network Card(s):               4 NIC(s) Installed.
                               [01]: Intel(R) 82574L Gigabit Network Connection
                                     Connection Name: Ethernet0
                                     IP address(es)
                                     [01]: 192.168.8.201
                                     [02]: fe80::aaa:1f68:e09e:1c84
                                     [03]: fd00::201
Hyper-V Requirements:           A hypervisor has been detected.
```

---

## PowerShell (Get-ComputerInfo)

```powershell
Get-ComputerInfo

WindowsProductName              : Windows 10 Home
OSDisplayVersion                : 25H2
CsManufacturer                  : VMware, Inc.
CsModel                         : VMware20,1
CsProcessors                    : {Intel(R) Core(TM) Ultra 9 185H}
CsTotalPhysicalMemory           : 8588775424
OsVersion                       : 10.0.26200
OsBuildNumber                   : 26200
OsHotFixes                      : {KB5087051, KB5054156, KB5094126, KB5094135}
OsLastBootUpTime                : 6/20/2026 7:15:59 PM
OsUptime                        : 03:07:22.0760098
TimeZone                        : (UTC-08:00) Pacific Time (US & Canada)
HyperVisorPresent                : True
DeviceGuardSmartStatus          : Off
```

Can also filter out results:
```powershell
Get-ComputerInfo | Select-Object WindowsProductName, OsVersion, OsBuildNumber, CsManufacturer, CsModel, CsProcessors, OsTotalVisibleMemorySize, OsFreePhysicalMemory, TimeZone
```

---

## Notes / Gotchas

- `Get-ComputerInfo` in powershell returns more fields than `systeminfo` in cmd