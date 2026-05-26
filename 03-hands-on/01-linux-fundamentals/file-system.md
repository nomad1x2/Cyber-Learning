# Linux File System

## Directory Reference

| Directory | Purpose |
|-----------|---------|
| `/`       | Root of the filesystem |
| `/bin`    | Essential user binaries (ls, cp, mv) |
| `/sbin`   | System binaries (root-only tools) |
| `/usr/bin`| User-installed binaries |
| `/usr/sbin`| Non-essential system binaries |
| `/usr/local/bin` | Optionally installed/compiled binaries |
| `/opt`    | Optional third-party software packages |
| `/etc`    | System-wide configuration files |
| `/var`    | Variable data (logs, mail, spool) |
| `/tmp`    | Temporary files, cleared on reboot |
| `/home`   | User home directories |
| `/root`   | Root user's home directory |
| `/lib`    | Shared essential libraries |
| `/dev`    | Device files |
| `/proc`   | Virtual filesystem for kernel/process info |
| `/sys`    | Virtual filesystem for hardware/driver info |
| `/mnt`    | Temporary mount points |
| `/media`  | Removable media mount points |

---

## Commands / Steps

### Where are binaries?
```bash
which ls
whereis ls
```

### Find user-installed binaries
```bash
ls /bin /usr/bin /usr/local/bin
```
### Find optionally installed packages
```bash
ls /opt
```
### Find system binaries
```bash
ls /sbin /usr/sbin /usr/local/sbin
```
---

## Screenshots

---

## Notes / Gotchas