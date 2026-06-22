#!/bin/bash

# shbang

# need root to update/upgrade and set interfaces
if [[ $EUID -ne 0 ]]; then
    echo "Run with sudo"
    exit 1
fi

# grab og user
USER=${SUDO_USER:-$(logname)}

# update on next reboot or no?
echo "[+] Configuring network interfaces..."

# this is the same config for the lab setup currently
cat > /etc/network/interfaces.d/lab-setup <<'EOF'
auto eth0
iface eth0 inet static
    address 192.168.8.200
    netmask 255.255.255.0
    gateway 192.168.8.1
    dns-nameservers 192.168.8.1
iface eth0 inet6 static
    address fd00::200
    netmask 64
    
auto eth1
iface eth1 inet static
    address 1.1.1.10
    netmask 255.255.255.0
EOF

# flush the eths
ip addr flush dev eth0
ip addr flush dev eth1

# reset the eths
ifdown eth0 && ifup eth0
ifdown eth1 && ifup eth1

# lets not update/upgrade til network is reachable
echo "[+] Waiting for network..."

until ping -c1 -W2 8.8.8.8 >/dev/null 2>&1; do
    sleep 1
done

# this needs root
echo "[+] Network reachable, updating..."
apt update && apt upgrade -y

# open firefox as current user in background
echo "[+] Opening Firefox..."
runuser -u "$USER" -- firefox &

# let him cook
sleep 2

# use my current terminator layour (its 2x2)
echo "[+] Opening Terminator..."

runuser -u "$USER" -- terminator -l quads &

# let him cook again
sleep 2

# kill oldest term to cleanup
pkill -u "$USER" -x terminator -o
