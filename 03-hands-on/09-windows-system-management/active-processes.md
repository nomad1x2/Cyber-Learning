# Active Processes


## CMD (tasklist)

List all running processes:
```cmd
tasklist

Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          8 K
svchost.exe                    908 Services                   0     38,412 K
explorer.exe                  4824 Console                    1    386,432 K
msedge.exe                    9180 Console                    1    185,988 K
```

Verbose output:
- adds status, username, CPU time, window title
```cmd
tasklist /v

Image Name      PID Session Name  Mem Usage  User Name                 CPU Time  Window Title
explorer.exe   4824 Console       386,528 K  DESKTOP-R4EM499\User03    0:01:31   New tab
cmd.exe        5820 Console         8,108 K  DESKTOP-R4EM499\User03    0:00:20   Administrator: Command Prompt
```

Filter by process name:
```cmd
tasklist /fi "imagename eq msedge.exe"

Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
msedge.exe                    9180 Console                    1    186,280 K
msedge.exe                    4328 Console                    1     13,196 K
```

---

## PowerShell (Get-Process)

List all processes:
```powershell
Get-Process

Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
   5113     142   181840     386460      91.86   4824   1 explorer
   1680      58    66124     187220       2.52   9180   1 msedge
```

Get path:
- shows where the process spawns from
```powershell
Get-Process msedge | Select-Object Name, Id, Path

Name      Id Path
----      -- ----
msedge  2060 C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
msedge  3332 C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
msedge  4328 C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

---

## tasklist Reference

| Flag | Description |
|---|---|
| `/V` | Verbose - adds status, username, CPU time, window title |
| `/SVC` | Shows services hosted in each process |
| `/M [module]` | Lists tasks using a given exe/dll; all modules if omitted |
| `/FI filter` | Filters output by criteria (see filters below) |
| `/FO format` | Output format - `TABLE`, `LIST`, or `CSV` |
| `/NH` | Suppresses column headers (TABLE/CSV only) |
| `/S system` | Query a remote system |

**Common filters (used with `/FI`):**
| Filter | Example |
|---|---|
| `IMAGENAME` | `tasklist /fi "imagename eq msedge.exe"` |
| `PID` | `tasklist /fi "pid eq 4824"` |
| `STATUS` | `tasklist /fi "status eq running"` |
| `MEMUSAGE` | `tasklist /fi "memusage gt 100000"` |
| `USERNAME` | `tasklist /fi "username ne NT AUTHORITY\SYSTEM"` |

**Examples:**
```cmd
tasklist /v
tasklist /svc
tasklist /fo csv
tasklist /fi "status eq running"
tasklist /fi "username ne NT AUTHORITY\SYSTEM" /fi "status eq running"
```

---

## Notes / Gotchas
- `tasklist` does not show executable path directly
  - Use PowerShell's `Get-Process | Select-Object Path` instead
- `tasklist /fi` filter syntax requires quotes around the filter string: `"imagename eq name.exe"`
- `Get-Process` shows `Id` not `PID` - same value but different column name
- Processes without a visible window show `N/A` for Window Title in `tasklist /v`
  - Running in background