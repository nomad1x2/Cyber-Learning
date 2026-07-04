# Network Security Devices

- Network security devices monitor, filter, and control traffic to detect and prevent threats
- Operate at different layers of the OSI model
- Defense in depth: layers work together

---

## Firewall

- Filters traffic based on rules
  - Allow or deny based on IP, port, protocol, state

- First line of defense into a network

| Type | What it do |
|------|-------------|
| Packet filtering | Inspects IP headers (IP, port, protocol) without state awareness |
| Stateful inspection | Tracks connection state; knows if a packet is part of an established session |
| Application layer | Inspects actual payload and tracks protocols like HTTP, DNS, SMB, etc |
| Next-gen firewall (NGFW) | Combines stateful + Application layer + IPS + threat intel + app awareness |
| WAF | Web Application Firewall - specifically filters HTTP/S traffic, blocks SQLi, XSS, etc |

```
Packet filtering:   [src IP] [dst IP] [port] [protocol] → allow/deny
Stateful:           above + tracks SYN/ACK state, blocks out-of-state packets
NGFW:               above + deep packet inspection + app ID + user ID
```

Common tools/vendors:
| Tool | Type |
|------|------|
| `iptables` / `nftables` | Linux host-based firewall |
| `pf` | BSD packet filter |
| pfSense | Open source NGFW |
| Palo Alto | Enterprise NGFW |
| Fortinet FortiGate | Enterprise NGFW |
| Cisco ASA | Enterprise stateful firewall |

---

## IDS / IPS

- IDS — Intrusion Detection System — monitors and alerts, does not block
- IPS — Intrusion Prevention System — monitors, alerts, and actively blocks
- Can be network-based (NIDS/NIPS) or host-based (HIDS/HIPS)

| Type | Where it sits | What it does |
|------|--------------|-------------|
| NIDS | Network tap / span port | Passively monitors network traffic |
| NIPS | Inline between segments | Actively blocks malicious traffic |
| HIDS | On the host | Monitors logs, file integrity, system calls |
| HIPS | On the host | Blocks malicious activity at host level |

Detection methods:

| Method | How it works |
|--------|-------------|
| Signature-based | Matches traffic against known attack signatures — fast but misses zero-days |
| Anomaly-based | Baselines normal behavior, flags deviations — catches unknowns but more false positives |
| Policy-based | Flags violations of defined security policy |
| Heuristic | Uses rules/algorithms to identify suspicious patterns |

Common tools:
| Tool | Type |
|------|------|
| Snort | Open source NIDS/NIPS |
| Suricata | Open source NIDS/NIPS — multi-threaded |
| Zeek (Bro) | Network analysis framework — logs and analysis |
| OSSEC | Open source HIDS |
| Wazuh | Open source HIDS/SIEM — built on OSSEC |

---

## EDR

- Endpoint Detection and Response
- Agent installed on endpoints — monitors processes, file system, network, registry
- Goes beyond AV — detects, investigates, and responds to threats on the host
- Key target for attackers — evading EDR is a major part of modern red teaming

| Capability | What it does |
|------------|-------------|
| Process monitoring | Tracks all running processes and their parent/child relationships |
| File system monitoring | Detects file creation, modification, deletion |
| Network monitoring | Tracks outbound connections from endpoints |
| Memory scanning | Detects injected code, shellcode in memory |
| Behavioral detection | Flags suspicious chains of activity |
| Threat hunting | Allows analysts to query telemetry across all endpoints |
| Response actions | Isolate host, kill process, delete file remotely |

Common EDR platforms:
| Platform | Vendor |
|----------|--------|
| CrowdStrike Falcon | CrowdStrike |
| Carbon Black | VMware |
| Defender for Endpoint | Microsoft |
| SentinelOne | SentinelOne |
| Cortex XDR | Palo Alto |

EDR evasion techniques (red team context):
| Technique | What it does |
|-----------|-------------|
| Process injection | Inject shellcode into a legitimate process |
| BYOVD | Bring Your Own Vulnerable Driver — exploit signed driver to disable EDR |
| Direct syscalls | Bypass EDR hooks in userspace by calling kernel directly |
| Living off the land (LOLBins) | Use built-in Windows tools — `certutil`, `rundll32`, `mshta` |
| Memory-only payloads | Never write to disk — evades file-based detection |

---

## SIEM

- Security Information and Event Management
- Aggregates logs from across the environment — correlates events to detect threats
- Central visibility platform for SOC analysts

| Component | What it does |
|-----------|-------------|
| Log aggregation | Collects logs from firewalls, endpoints, servers, apps |
| Normalization | Converts logs to common format for analysis |
| Correlation rules | Matches patterns across multiple log sources to detect attacks |
| Alerting | Notifies analysts when rules fire |
| Dashboards | Visual overview of security posture |
| Retention | Long-term log storage for forensics and compliance |

Common SIEMs:
| Platform | Notes |
|----------|-------|
| Splunk | Most widely used enterprise SIEM |
| IBM QRadar | Enterprise SIEM |
| Elastic SIEM | Open source — built on ELK stack |
| Microsoft Sentinel | Cloud-native SIEM — Azure |
| Wazuh | Open source — good for home labs |

---

## PSP (Personal Security Products)

- Security software running on individual endpoints
- Includes antivirus, anti-malware, host firewall, DLP

| Type | What it does |
|------|-------------|
| Antivirus (AV) | Signature-based detection of known malware |
| Anti-malware | Broader — includes behavioral detection |
| Host firewall | Controls inbound/outbound traffic on the host |
| DLP | Data Loss Prevention — prevents sensitive data leaving the endpoint |
| Application whitelisting | Only allows approved applications to run |

Detection methods:
| Method | How it works |
|--------|-------------|
| Signature | Hash or pattern match against known malware database |
| Heuristic | Flags code that behaves like malware without a known signature |
| Behavioral | Monitors runtime behavior — flags suspicious actions |
| Sandboxing | Executes file in isolated environment to observe behavior |

---

## Common Detection & Prevention Techniques

| Technique | What it does |
|-----------|-------------|
| Deep packet inspection (DPI) | Inspects packet payload, not just headers |
| TLS inspection | Decrypts and inspects encrypted traffic |
| Honeypots | Decoy systems — attract and detect attackers |
| Network segmentation | Isolates segments — limits lateral movement |
| Zero trust | Never trust, always verify — every request authenticated |
| Threat intel feeds | Live feeds of known malicious IPs, domains, hashes |
| UEBA | User and Entity Behavior Analytics — detects anomalous user behavior |

---

## References
- [NIST SP 800-94 — IDS/IPS Guide](https://csrc.nist.gov/publications/detail/sp/800-94/final)
- [CrowdStrike — What is EDR?](https://www.crowdstrike.com/cybersecurity-101/endpoint-security/endpoint-detection-and-response-edr/)
- [Palo Alto — What is a NGFW?](https://www.paloaltonetworks.com/cyberpedia/what-is-a-next-generation-firewall)
