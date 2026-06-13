
# OpenVPN

## Debian VM – OpenVPN Server

Using nmcli to configure interfaces, then setting up OpenVPN using Easy-RSA for certificates:

### Steps

- Enable IP forwarding:

```bash
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sudo sysctl -p
```

- Install OpenVPN and Easy-RSA:
- Ref:
  - https://easy-rsa.readthedocs.io/en/latest/
  - https://linuxconfig.org/vpn-virtual-private-network-and-openvpn

```bash
sudo apt update
sudo apt install openvpn easy-rsa -y
```

- Set up the PKI and build the certificate authority:

```bash
make-cadir ~/easy-rsa
cd ~/easy-rsa
./easyrsa init-pki
./easyrsa build-ca nopass
```

- Generate and sign the server certificate:

```bash
./easyrsa gen-req server nopass
./easyrsa sign-req server server
./easyrsa gen-dh
```

- Generate and sign the Win11 client certificate:

```bash
./easyrsa gen-req win11client nopass
./easyrsa sign-req client win11client
```

- Copy server certs to `/etc/openvpn/` so the service can access them:

```bash
sudo cp ~/easy-rsa/pki/ca.crt /etc/openvpn/
sudo cp ~/easy-rsa/pki/issued/server.crt /etc/openvpn/
sudo cp ~/easy-rsa/pki/private/server.key /etc/openvpn/
sudo cp ~/easy-rsa/pki/dh.pem /etc/openvpn/
```

- Copy client certs just to home directory so client can pull them easily:

```bash
sudo cp -p ~/easy-rsa/pki/ca.crt ~/
sudo cp -p ~/easy-rsa/pki/issued/win11client.crt ~/
sudo cp -p ~/easy-rsa/pki/private/win11client.key ~/
```


- Create `/etc/openvpn/server.conf`:

```
port 1194
proto udp
dev tun
ca /etc/openvpn/ca.crt
cert /etc/openvpn/server.crt
key /etc/openvpn/server.key
dh /etc/openvpn/dh.pem
topology subnet
server 172.16.20.0 255.255.255.0
push "route 2.2.2.0 255.255.255.0"
keepalive 10 120
persist-key
persist-tun
verb 3
```

- Start OpenVPN:

```bash
sudo systemctl start openvpn@server
sudo systemctl enable openvpn@server
sudo systemctl status openvpn@server
```

- Transfer client certs to Win11 with SCP (Win11 PowerShell):

```powershell
scp User01@192.168.8.203:~/ca.crt "C:\Program Files\OpenVPN Connect\config"
scp User01@192.168.8.203:~/win11client.crt "C:\Program Files\OpenVPN Connect\config"
scp User01@192.168.8.203:~/win11client.key "C:\Program Files\OpenVPN Connect\config"
```

### Commands ran:
`sudo apt install openvpn easy-rsa` - install packages  
`./easyrsa init-pki / build-ca / gen-req / sign-req / gen-dh` - build PKI and certs  
`sudo systemctl start openvpn@server` - start service  
`sudo systemctl status openvpn@server` - verify running  

---

## Win11 VM – OpenVPN Client

Connecting to the Debian OpenVPN server.

### Steps

- Download and install OpenVPN GUI
- Create the `win11client.ovpn` config:

```
client
dev tun
proto udp
remote 192.168.8.203 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert win11client.crt
key win11client.key
verb 3
```

- Move the files into the `C:\Program Files\OpenVPN Connect\config` directory
- Import OpenVPN profile into the GUI and connect (or double click new .ovpn file)

- Verify the tunnel is up:

```powershell
ping 172.16.20.1 (debian, tun0 interface - peer)
ping 2.2.2.40 (debian, ens37 interface - network)
```

### Commands ran:
`ping` - test connectivity through tunnel  