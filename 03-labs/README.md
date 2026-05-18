# Labs

## Environment

Current lab setup consists of two host machines:

- Laptop 1: Hypervisor hosting Windows 11 + Kali Linux VMs (WiFi)
- Laptop 2: Hypervisor hosting Debian + Ubuntu VMs (Ethernet cable)

Network infrastructure:
- GL.iNet wireless router
- Tethered internet setup
- All VMs configured via DHCP

Hypervisor platform:
- VMware

---

## Known Issues / Notes

- Laptop 1 physical bridge instability when using wired Ethernet -- switched to WiFi bridge
- Kali Linux VM: mouse input issue resolved by upgrading VM hardware compatibility to 17.5+
- Windows 11 firewall blocked ping by default (ICMP disabled inbound)

---

## Directory Layout

```text
03-labs/
├── debian/
├── kali/
├── ubuntu/
└── windows/