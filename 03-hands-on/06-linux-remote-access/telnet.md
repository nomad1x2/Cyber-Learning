
# Telnet

## Overview

Telnet is used to establish a remote terminal where data is passed over plaintext
- Dont use Telnet
- BUT, it can also be used for banner grabbing

---

## Commands / Steps

```bash
# Connect to a host running telnet
telnet 192.168.8.50

# Banner grab - connect to a specific port and read the service response
┌──(nomad㉿kali)-[~/telnet]
└─$ telnet 192.168.8.50 2222 
Trying 192.168.8.50...
Connected to 192.168.8.50.
Escape character is '^]'.
SSH-2.0-OpenSSH_10.0p2 Raspbian-7+deb13u4

Invalid SSH identification string.
Connection closed by foreign host.


┌──(nomad㉿kali)-[~/telnet]
└─$ telnet 192.168.8.202 22  
Trying 192.168.8.202...
Connected to 192.168.8.202.
Escape character is '^]'.
SSH-2.0-OpenSSH_10.2p1 Ubuntu-2ubuntu3.2

Invalid SSH identification string.
Connection closed by foreign host.
```

The banner revealed the service, version, and OS without authenticating and before terminating the session

---

## Use Cases
- **Banner grabbing** - identify what service and version is running on a port
- **Port testing** - quick check if a port is open and responding
- **Legacy systems** - some older network equipment might still expose telnet for management

## Limitations
- **Plaintext** - all data including passwords sent unencrypted
- **No integrity checking** - traffic can be modified in transit

---

## Notes / Gotchas
- `Connection refused` means the host is up but nothing is listening on that port - not that the host is down
- Can also use `nc` for the same banner grabbing with more control: `nc -v 192.168.8.202 22`
```bash
                                                                                                                                                                                                                                            
┌──(nomad㉿kali)-[~/telnet]
└─$ nc -v 192.168.8.202 22
192.168.8.202: inverse host lookup failed: Unknown host
(UNKNOWN) [192.168.8.202] 22 (ssh) open
SSH-2.0-OpenSSH_10.2p1 Ubuntu-2ubuntu3.2

Invalid SSH identification string.
                                                                                                                                                                                                                                            
┌──(nomad㉿kali)-[~/telnet]
└─$ nc -v 192.168.8.50 2222 
192.168.8.50: inverse host lookup failed: Unknown host
(UNKNOWN) [192.168.8.50] 2222 (?) open
SSH-2.0-OpenSSH_10.0p2 Raspbian-7+deb13u4

Invalid SSH identification string.
```