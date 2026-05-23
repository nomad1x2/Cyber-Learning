
# WireGuard

## Ubuntu VM – WireGuard Server

Setting up WireGuard as the tunnel server on Ubuntu:

### Steps

- Install WireGuard:

```bash
sudo apt update
sudo apt install wireguard -y
```

- Generate keys:

```bash
wg genkey > /etc/wireguard/privatekey
wg pubkey < /etc/wireguard/privatekey > /etc/wireguard/publickey
cat /etc/wireguard/privatekey
cat /etc/wireguard/publickey
```

- Create `/etc/wireguard/wg0.conf` - Ubuntu is the server with IP `10.0.0.1`:

```ini
[Interface]
Address = 10.0.0.1/30
ListenPort = 51820
PrivateKey = <ubuntu_private_key>

[Peer]
PublicKey = <kali_public_key>
AllowedIPs = 10.0.0.2/32, 1.1.1.0/24
```

- Bring up the tunnel:

```bash
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
wg show
```

### Commands ran:
`sudo apt install wireguard` - install WireGuard  
`wg genkey` / `wg pubkey` - generate keypair  
`sudo wg-quick up wg0` - start tunnel  
`wg show` - verify handshake  

---

## Kali VM – WireGuard Client

Completing the WireGuard tunnel from the Kali side:

### Steps

- Install WireGuard:

```bash
sudo apt update
sudo apt install wireguard -y
```

- Generate keys:

```bash
wg genkey > /etc/wireguard/privatekey
wg pubkey < /etc/wireguard/privatekey > /etc/wireguard/publickey
cat /etc/wireguard/privatekey
cat /etc/wireguard/publickey
```

- Create `/etc/wireguard/wg0.conf` - Kali is the client at tunnel IP `10.0.0.2`, connecting to Ubuntu:

```ini
[Interface]
Address = 10.0.0.2/30
PrivateKey = <kali_private_key>

[Peer]
PublicKey = <ubuntu_public_key>
Endpoint = 192.168.8.202:51820
AllowedIPs = 10.0.0.1/32, 2.2.2.0/24
PersistentKeepalive = 25
```

- Bring up the tunnel and test:

```bash
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
wg show
ping 10.0.0.1 (ubuntu wg0)
ping 2.2.2.30 (ubuntu ens37)
```

### Commands ran:
`sudo apt install wireguard` - install WireGuard  
`wg genkey` / `wg pubkey` - generate keypair  
`sudo wg-quick up wg0` - start tunnel  
`wg show` - verify handshake  
`ping` - test connectivity through tunnel 