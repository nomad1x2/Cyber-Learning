# Log Files & Locations

## Log levels

|Level|Num|Description|
|----|----|----|
|Emergency| 0|System is unusable|
|Alert| 1|Action must be taken immediately|
|Critical| 2|Critical conditions|
|Error| 3|Error conditions|
|Warning| 4|Warning conditions|
|Notice| 5|Normal but significant condition|
|Info| 6|Informational messages|
|Debug| 7|Debug-level messages|

## dmesg

Dmesg is used to examine or control the kernel ring buffer
- The kernel ring buffer is a circular buffer in memory where the Linux kernel stores important messages. It is a fixed-size buffer, and once it reaches its maximum capacity, new messages overwrite the oldest ones. The buffer stores messages related to various kernel activities, such as hardware initialization, driver loading, and system events.

You can use it to troubleshoot hardware issues, monitor system events, and track system boot process

Ref:
- https://linuxvox.com/blog/linux-dmesg/

```bash
# Use default to display all messages from the kernel ring buffer
dmesg

# Display kernel messages
dmesg -k

# Use syslog rather than /dev/kmsg
dmesg -S

# Display userspace messages (non-kernel)
dmesg -u

# Show local time and time delta in readable format
dmesg -e

# Display human readable timestamps (may be inaccurate)
dmesg -T
```

---

## syslog

Syslog is a standard for message logging that allows various parts of a system to send log messages to a central location

It essentially collects a wider slice of daemon and system messages

On Debian/Ubuntu the path is `/var/log/syslog`, but on RHEL/CentOS/Fedora it's `/var/log/messages`

On systems using systemd-journald, some logs may not hit `/var/log/syslog` at all unless rsyslog is also running and configured to forward them

Refs:
- https://linuxvox.com/blog/linux-syslog/
- https://www.digitalocean.com/community/tutorials/how-to-monitor-system-authentication-logs-on-ubuntu

---

## wtmp

`wtmp` is a binary file that stores information about user logins, logouts, system boots, and shutdowns in a structured format
- Located in `/var/log/wtmp*` (* includes log rotating)

Ref:
- https://linuxvox.com/blog/wtmp-linux/

```bash
# Use to see who logged in recently (all or specific)
last USER

# Use to see last successful login per user (replaced with lastlog2)
lastlog -u USER
```

`last` searches back through the `/var/log/wtmp` file (or the file designated by the -f option) and displays a list of all users logged in (and out) since that file was created. One or more usernames and/or ttys can be given, in which case last will show only the entries matching those arguments

`lastlog` to view only most recent logins and times in `/var/log/lastlog` (may be replaced by `/var/log/lastlog2`)

---

## btmp

`btmp` is similar to `wtmp`, but stores information about bad login attemps
- Located in `/var/log/btmp*` (* for rotating logs)

Ref:
- https://linuxhandbook.com/utmp-wtmp-btmp/


```bash
# Use to show a log of bad login attempts
lastb
```

`lastb` is similar to `last`, except that by default it shows a log of the `/var/log/btmp` file, which contains all the bad login attempts

---

## auth.log

`/var/log/auth.log` contains authentication and privilege events
- Used to track priv esc with sudo / su, and detect failed logins / authentication failures

Ref:
- https://www.digitalocean.com/community/tutorials/how-to-monitor-system-authentication-logs-on-ubuntu

---

## Notes / Gotchas

- Since `wtmp` and `btmp` are binary files, strings won't really work