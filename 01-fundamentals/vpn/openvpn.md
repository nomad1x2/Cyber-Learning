
# OpenVPN

## Debian VM – OpenVPN Server

Using nmcli to configure interfaces, then setting up OpenVPN using Easy-RSA for certificates:

### Steps

- Enable IP forwarding:

```bash
echo "net.ipv4.ip_forward=1" > /etc/sysctl.conf
sudo sysctl -p
```

- Install OpenVPN and Easy-RSA:

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

- Copy certs to `/etc/openvpn/` so the service can access them:

```bash
sudo cp ~/easy-rsa/pki/ca.crt /etc/openvpn/
sudo cp ~/easy-rsa/pki/issued/server.crt /etc/openvpn/
sudo cp ~/easy-rsa/pki/private/server.key /etc/openvpn/
sudo cp ~/easy-rsa/pki/dh.pem /etc/openvpn/
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
server 10.2.0.0 255.255.255.0
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
scp User01@192.168.8.203:/home/User01/ca.crt C:\Users\User03\Desktop\
scp User01@192.168.8.203:/home/User01/win11client.crt C:\Users\User03\Desktop\
scp User01@192.168.8.203:/home/User01/win11client.key C:\Users\User03\Desktop\
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
- Import OpenVPN profile into the GUI
- The `win11client.ovpn` config:

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

- Verify the tunnel:

```powershell
ping 10.2.0.1 (debian - tun0 peer)
ping 2.2.2.40 (debian - ens37)
```

### Commands ran:
`ping` - test connectivity through tunnel  