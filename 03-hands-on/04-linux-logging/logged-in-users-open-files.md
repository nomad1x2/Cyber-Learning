# Logged-In Users & Open Files (who, lsof)

## Overview

`who` - show logged in users and login sessions
`w` - show logged in users, system load, and what users are running
`lsof` - list open files, sockets, devices, and network connections

---

## who/w

```bash
# Who is logged in and from where
┌──(nomad㉿kali)-[~]
└─$ who -a
           system boot  2026-06-09 19:49
nomad    ? seat0        2026-06-09 19:52   ?          1353 (:0)


# Who is logged in + system load + what they're running
┌──(nomad㉿kali)-[~]
└─$ w     
 20:13:53 up 24 min,  1 user,  load average: 0.08, 0.06, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU  WHAT
nomad             -                19:52           0.00s   ?    lightdm --session-child 13 24
```

|Flag|Description|
|----|----|
|`-a, --all `|same as -b -d --login -p -r -t -T -u|
|`-b, --boot`|time of last system boot|
|`-l, --login`|print system login processes|
|`-p, --process`|print active processes spawned by init|
|`-q, --count`|all login names and number of users logged on|
|`-u, --users`|list users logged in, including idle time|

---

## lsof

```bash
# All files opened by a user
┌──(nomad㉿kali)-[~]
└─$ sudo lsof -u nomad | head -5
lsof: WARNING: can't stat() fuse.gvfsd-fuse file system /run/user/1001/gvfs
      Output information may be incomplete.
COMMAND     PID  USER  FD      TYPE             DEVICE  SIZE/OFF       NODE NAME
systemd    1377 nomad cwd       DIR                8,1      4096          2 /
systemd    1377 nomad rtd       DIR                8,1      4096          2 /
systemd    1377 nomad txt       REG                8,1    141696    4101113 /usr/lib/systemd/systemd
systemd    1377 nomad mem       REG                8,1    182560    4356316 /usr/lib/x86_64-linux-gnu/libseccomp.so.2.6.0


# All open network connections (with process names)
┌──(nomad㉿kali)-[~]
└─$ sudo lsof -i
COMMAND   PID USER FD   TYPE DEVICE SIZE/OFF NODE NAME
rsyslogd  530 root  6u  IPv4  10715      0t0  TCP *:shell (LISTEN)
rsyslogd  530 root  7u  IPv6  10716      0t0  TCP *:shell (LISTEN)
rsyslogd  530 root 15u  IPv4  23284      0t0  TCP 192.168.8.200:shell->192.168.8.50:39432 (ESTABLISHED)
sshd     1096 root  6u  IPv4  15378      0t0  TCP *:ssh (LISTEN)
sshd     1096 root  7u  IPv6  15380      0t0  TCP *:ssh (LISTEN)

# Who is using a specific port
┌──(nomad㉿kali)-[~]
└─$ sudo lsof -i :22
COMMAND  PID USER FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd    1096 root 6u  IPv4  15378      0t0  TCP *:ssh (LISTEN)
sshd    1096 root 7u  IPv6  15380      0t0  TCP *:ssh (LISTEN)

┌──(nomad㉿kali)-[~]
└─$ sudo lsof -iTCP -sTCP:LISTEN
COMMAND   PID USER FD   TYPE DEVICE SIZE/OFF NODE NAME
rsyslogd  530 root 6u  IPv4  10715      0t0  TCP *:shell (LISTEN)
rsyslogd  530 root 7u  IPv6  10716      0t0  TCP *:shell (LISTEN)
sshd     1096 root 6u  IPv4  15378      0t0  TCP *:ssh (LISTEN)
sshd     1096 root 7u  IPv6  15380      0t0  TCP *:ssh (LISTEN)
```

|lsof Column|Description|
|----|----|
|`COMMAND`|Process name|
|`PID`|Process ID|
|`FD`|File descriptor used by the process|
|`TYPE`|File type (REG, DIR, IPv4, IPv6, etc)|
|`NAME`|File path, socket, network connection|

|Flag|Description|
|----|----|
|`-i`|Display network files/sockets (TCP, UDP, IPv4, IPv6)|
|`-p <PID>`|Show files and sockets opened by a specific process|
|`-u <USER>`|Show files and sockets owned by a specific user|
|`-n`|Don't resolve hostnames (show IP addresses)|
|`-P`|Don't resolve port numbers to service names|

|FD Value|Description|
|----|----|
|`cwd`|Current working directory|
|`rtd`|Root directory|
|`txt`|Program executable|
|`mem`|Memory-mapped file/library|
|`0u`|stdin|
|`1u`|stdout|
|`2u`|stderr|

---

## Notes / Gotchas

- `lsof` needs sudo to see files owned by other users
- `lsof -i :PORT` is useful for identifying what process is using a port
- `lsof -iTCP -sTCP:LISTEN` shows services actively listening for connections