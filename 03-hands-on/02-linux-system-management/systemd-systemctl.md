# systemd & systemctl

## Overview

### System and Service Manager

Ref:
- https://systemd.io/

"systemd is a suite of basic building blocks for a Linux system. It provides a system and service manager that runs as PID 1 and starts the rest of the system.

systemd provides aggressive parallelization capabilities, uses socket and D-Bus activation for starting services, offers on-demand starting of daemons, keeps track of processes using Linux control groups, maintains mount and automount points, and implements an elaborate transactional dependency-based service control logic."

### Basically, 

`systemd` is the first process started by the kernel (with PID 1) and initializes the components that need to be started after the kernel is booted. Its the daemon responsible for Service Management while the OS is running.

Consists of `service units` and `target units` 
- `Service Unit`: for managing daemons
- `Target Unit`: a 'collection' of other units

`systemd` is the daemon/service running as PID 1 that manages services
`systemctl` is how we _talk_ to `systemd`

---

## Commands / Steps

```bash
┌──(nomad㉿nomad)-[~]
└─$ ps --pid 1
    PID TTY          TIME CMD
      1 ?        00:00:00 systemd

┌──(nomad㉿nomad)-[~]
└─$ ps --ppid 1
    PID TTY          TIME CMD
      2 ?        00:00:00 init-systemd(ka
     48 ?        00:00:00 systemd-journal
     57 ?        00:00:00 systemd-udevd
     88 ?        00:00:00 cron
     93 ?        00:00:00 dbus-daemon
    115 ?        00:00:00 systemd-logind
    247 ?        00:00:01 containerd
    251 hvc0     00:00:00 agetty
    252 tty1     00:00:00 agetty
    270 ?        00:00:00 dockerd
    515 ?        00:00:00 systemd
```

|Command|Description|
|----|----|
|`systemctl`| Lists _all_ loaded units and their current state |
|`systemctl --type=service`| Lists services only |
|`systemctl --state=active`| Lists everything currently running |
|`systemctl --state=failed`| Lists anything broken |
|`systemctl status ssh`| Lists detailed info/logs for the _ssh_ service |
|`systemctl enable ssh`| Starts the _ssh_ service at _boot_ |
|`systemctl disable ssh`| Does _not_ start the _ssh_ service at _boot_ |
|`systemctl start ssh`| Starts the _ssh_ service |
|`systemctl stop ssh`| Stops the _ssh_ service |
|`systemctl restart ssh`| Restarts the _ssh_ service |
|`systemctl cat ssh`| Prints the _ssh_ unit file contents and its path |

### Examples

```bash
┌──(nomad㉿nomad)-[~]
└─$ sudo systemctl status ssh
○ ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; disabled; preset: disabled)
     Active: inactive (dead)
       Docs: man:sshd(8)
             man:sshd_config(5)

┌──(nomad㉿nomad)-[~]
└─$ sudo systemctl enable ssh
Synchronizing state of ssh.service with SysV service script with /usr/lib/systemd/systemd-sysv-install.
Executing: /usr/lib/systemd/systemd-sysv-install enable ssh
Created symlink '/etc/systemd/system/sshd.service' → '/usr/lib/systemd/system/ssh.service'.
Created symlink '/etc/systemd/system/multi-user.target.wants/ssh.service' → '/usr/lib/systemd/system/ssh.service'.

┌──(nomad㉿nomad)-[~]
└─$ sudo systemctl start ssh

┌──(nomad㉿nomad)-[~]
└─$ sudo systemctl status ssh
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; enabled; preset: disabled)
     Active: active (running) since Fri 2026-06-05 19:50:06 CDT; 2s ago
 Invocation: 617e65b14a234091a970befbcc04f01e
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 1551 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 1553 (sshd)
      Tasks: 1 (limit: 13995)
     Memory: 5.1M (peak: 5.8M)
        CPU: 22ms
     CGroup: /system.slice/ssh.service
             └─1553 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"

Jun 05 19:50:06 nomad systemd[1]: Starting ssh.service - OpenBSD Secure Shell server...
Jun 05 19:50:06 nomad sshd[1553]: Server listening on 0.0.0.0 port 22.
Jun 05 19:50:06 nomad sshd[1553]: Server listening on :: port 22.
Jun 05 19:50:06 nomad systemd[1]: Started ssh.service - OpenBSD Secure Shell server.
```

---

|Path|What it is|
|----|----|
|`/usr/lib/systemd/system/`| Package default; installed by apt/dnf |
|`/etc/systemd/system/`| User overrides; manually edit here. Takes precedence over the above |
|`/etc/systemd/system/<unit>.d/`| Partial overrides without replacing the whole file |

---

### Systemctl cat:

```bash
┌──(nomad㉿nomad)-[~]
└─$ systemctl cat ssh
# /usr/lib/systemd/system/ssh.service
[Unit]
Description=OpenBSD Secure Shell server
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target nss-user-lookup.target auditd.service
ConditionPathExists=!/etc/ssh/sshd_not_to_be_run

[Service]
EnvironmentFile=-/etc/default/ssh
ExecStartPre=/usr/sbin/sshd -t
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
ExecReload=/usr/sbin/sshd -t
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255
Type=notify
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
Alias=sshd.service
```

### cat /usr***/*.service:
```bash
┌──(nomad㉿nomad)-[~]
└─$ cat /usr/lib/systemd/system/ssh.service
[Unit]
Description=OpenBSD Secure Shell server
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target nss-user-lookup.target auditd.service
ConditionPathExists=!/etc/ssh/sshd_not_to_be_run

[Service]
EnvironmentFile=-/etc/default/ssh
ExecStartPre=/usr/sbin/sshd -t
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
ExecReload=/usr/sbin/sshd -t
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255
Type=notify
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
Alias=sshd.service
```

---

## Notes / Gotchas

- If making changes manually, make them in `/etc/systemd/system/` so package updates don't wipe edits, then run `systemctl daemon-reload` to apply them
- `systemctl enable` works by creating a symlink in `/etc/systemd/system/` pointing to the unit file in `/usr/lib/systemd/system/`. `systemctl disable` removes that symlink. The service itself is not modified, only changing whether it loads at boot