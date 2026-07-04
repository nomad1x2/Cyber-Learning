# Network Security Devices

- "Defense in depth" helps layers work together, meaning not JUST headers are inspected

## Firewall

- Filters traffic based on rules
  - Allow or deny based on IP, port, protocol, state
  
- Usually first line of defense into a network

| Type | What it does |
|------|-------------|
| Packet filtering | Inspects headers only (IP, port, protocol, no state awareness, etc) |
| Stateful inspection | Tracks connection state, knows if a packet is part of an established session |
| Application layer (L7) | Inspects payload and understands protocols like HTTP, DNS, SMB |
| Next-gen firewall (NGFW) | Combines stateful + L7 + IPS + threat intel + app awareness |
| Web Application Firewall (WAF) | Filters HTTP/S specifically, blocks SQLi, XSS, other web vulns |

Common firwalls/tools:

| Tool | Type |
|------|------|
| `iptables` / `nftables` | Linux host based firewall |
| Microsoft Defender | Malware protection, web protection, real-time security notifications, and security tips |
| pfSense | Open source NGFW |
| Palo Alto | Enterprise NGFW |
| Cisco FTD | Enterprise NGFW (replaced older ASA, managed by an FMC) |

Refs:
- https://linux.die.net/man/8/iptables
- https://support.microsoft.com/en-us/defender/getting-started-with-microsoft-defender
- https://www.pfsense.org/
- https://www.cloudflare.com/learning/security/what-is-next-generation-firewall-ngfw/
- https://www.paloaltonetworks.com/cyberpedia/what-is-a-next-generation-firewall-ngfw
- https://www.cisco.com/site/us/en/products/security/firewalls/firepower-1000-series/index.html

## IDS / IPS

Intrusion Detection System
- Monitors and alerts, does not block

Intrusion Prevention System
- Monitors, alerts, and actively blocks

- Network based (NIDS/NIPS)
- Host based (HIDS/HIPS)

| Type | Where it sits | What it does |
|------|--------------|-------------|
| NIDS | Network tap / span port | Passively monitors network traffic |
| NIPS | Inline between segments | Actively blocks network traffic |
| HIDS | On the host | Monitors logs, file integrity, system calls |
| HIPS | On the host | Blocks malicious activity at host level |

Common tools:

| Tool | Type |
|------|------|
| Snort | Open source NIDS/NIPS |
| Suricata | Open source NIDS/NIPS |
| Zeek | Network analysis framework for logs and analysis |
| Arkime | Open source network analysis and packet capture |
| Wireshark | More passive/manual analysis but i'd categorize it here also |

Refs:
- https://www.snort.org/
- https://suricata.io/
- https://zeek.org/
- https://arkime.com/
- https://www.wireshark.org/

## Endpoint Detection and Response (EDR)

Endpoint Detection and Response
- Agent installed on endpoints monitoring processes, file system, network, registry
- Detects, investigates, and responds to threats on the host

| Capability | What it does |
|------------|-------------|
| Process monitoring | Tracks all running processes and parent/child relationships |
| File system monitoring | Detects file creation, modification, deletion |
| Network monitoring | Tracks outbound connections from endpoints |
| Memory scanning | Detects injected code, shellcode in memory |
| Behavioral detection | Flags suspicious chains of activity |
| Response actions | Isolate host, kill process, delete files remotely |

Common platforms:

| Platform | Vendor |
|----------|--------|
| CrowdStrike Falcon | CrowdStrike |
| Defender for Endpoint | Microsoft |
| SentinelOne | SentinelOne |

Refs:
- https://www.crowdstrike.com/en-us/cybersecurity-101/endpoint-security/endpoint-detection-and-response-edr/
- https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint
- https://www.sentinelone.com/cybersecurity-101/endpoint-security/what-is-endpoint-detection-and-response-edr/

## Security Information and Event Management (SIEM)

- Aggregates/ingests/correlates/centralizes logs from across the network
- Central platform for analysts

| Component | What it does |
|-----------|-------------|
| Log aggregation | Collects logs from firewalls, endpoints, servers, apps, etc |
| Normalization | Converts logs to common format |
| Correlation rules | Matches patterns across sources to detect attacks |
| Alerting | Notifies when rules fire |
| Retention | Long term log storage for forensics |

Common platforms:

| Platform | Notes |
|----------|-------|
| Splunk | Most widely used enterprise SIEM |
| Elastic SIEM | Open source, built on ELK stack |
| Security Onion | Open source, built for network security monitoring, includes Zeek, Suricata, Elastic -- unsure if qualifies as a SIEM but i'm qualifying it as a SIEM |

Refs:
- https://www.splunk.com/en_us/blog/learn/siem-security-information-event-management.html
- https://www.elastic.co/elastic-stack/
- https://securityonionsolutions.com/software/

## Personal Security Products

- Security software running on individual endpoints
- Antivirus/malware, host firewall, DLP, etc

| Type | What it does |
|------|-------------|
| Antivirus | Signature based detection of known malware |
| Anti malware | Includes behavioral detection |
| Host firewall | Controls inbound/outbound traffic on the host |
| Data Loss Prevention (DLP) | Prevents sensitive data leaving the endpoint |
| Application whitelisting | Only allows approved applications to run |

Refs:
- https://www.fortinet.com/resources/cyberglossary/what-is-endpoint-security
- https://us.norton.com/blog/malware/what-is-antivirus
- https://www.ibm.com/think/topics/data-loss-prevention

## Detection Methods

| Method | How it works |
|--------|-------------|
| Signatures | Matches traffic against known attack signatures (misses zero days) |
| Anomaly | Baselines normal behavior, flags deviations (catches unknowns but more false positives) |
| Heuristic | Uses rules to identify suspicious patterns |
| Policy | Flags violations of defined security policy |
| Behavioral | Monitors runtime behavior flagging suspicious action chains (also manually with debuggers) |
| Sandboxing | Executes files in isolated environment to observe behavior |

Refs:
- https://www.sentinelone.com/cybersecurity-101/threat-intelligence/what-is-malware-detection/
- https://www.crowdstrike.com/en-us/cybersecurity-101/malware/malware-detection/

## Evasion Techniques

| Technique | What it does |
|-----------|-------------|
| Process injection | Inject shellcode into a legitimate process |
| Bring Your Own Vulnerable Driver (BYOVD) | Exploit signed driver to disable EDR |
| Direct syscalls | Bypass EDR hooks in userspace by calling kernel directly |
| LOLBins | Use builtin Windows tools like `certutil`, `rundll32`, `mshta` |
| Memory only payloads | Never write to disk and evade file based detection |
| Obfuscation / encoding / packing / encrypting | Editing payload/file size/hash to avoid signature matching |
| Traffic blending | Using common ports/protocols to hide/blend in C2 traffic |

Refs:
- https://attack.mitre.org/techniques/T1055/
- https://attack.mitre.org/techniques/T1068/
- https://www.paloaltonetworks.com/blog/security-operations/a-deep-dive-into-malicious-direct-syscall-detection/ (detection, but can research for "how its made")
- https://lolbas-project.github.io/
- https://deepstrike.io/blog/what-is-fileless-malware (again, detection but look at those cool examples)
- https://attack.mitre.org/techniques/T1027/
- https://attack.mitre.org/techniques/enterprise/

# Notes
- I hate kibana and its KQL