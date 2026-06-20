# Kill Active Applications

## tasklist - List Running Applications

List only running processes:
```cmd
tasklist /fi "STATUS eq RUNNING"

Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
explorer.exe                  4824 Console                    1    381,872 K
msedge.exe                    9180 Console                    1    195,764 K
msedge.exe                    4328 Console                    1     13,212 K
```

---

## taskkill - Terminate by Name

Kill all processes matching an image name:
```cmd
taskkill /im msedge.exe

SUCCESS: Sent termination signal to the process "msedge.exe" with PID 9180.
SUCCESS: Sent termination signal to the process "msedge.exe" with PID 4328.
ERROR: The process "msedge.exe" with PID 10492 could not be terminated.
Reason: This process can only be terminated forcefully (with /F option).
```

---

## taskkill - Terminate by PID

Force kill a specific process by its PID:
```cmd
taskkill /pid 8908 /F

SUCCESS: The process with PID 8908 has been terminated.
```

---

## taskkill - Force Kill with Child Processes

Force kill a process and all of its spawned children:
```cmd
taskkill /im msedge.exe /F /t

SUCCESS: The process with PID 5100 (child process of PID 1848) has been terminated.
SUCCESS: The process with PID 8136 (child process of PID 1848) has been terminated.
ERROR: The process with PID 4972 (child process of PID 1848) could not be terminated.
Reason: There is no running instance of the task.
SUCCESS: The process with PID 1848 (child process of PID 4824) has been terminated.
```

Verify everything is gone:
```cmd
tasklist /fi "imagename eq msedge.exe"

INFO: No tasks are running which match the specified criteria.
```

---

## taskkill Flags

| Flag | Description |
|---|---|
| `/im` | Target by image name (process name) |
| `/pid` | Target by specific process ID |
| `/F` | Force termination - required for processes that resist normal kill |
| `/T` | Tree kill - terminates the process and all child processes it spawned |

---

## Notes / Gotchas
- Without `/F`, some processes refuse to be killed with "can only be terminated forcefully"
  - Cmmon for apps with active state or unsaved work
- `/T` kills the entire process tree
- "There is no running instance of the task" error during a `/T` kill means that specific child process already exited
- Killing by `/im` targets every process with that name
  - if multiple unrelated apps share an image name, all instances die
