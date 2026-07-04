
# Lockheed Martin Cyber Kill Chain

Framework developed by Lockheed Martin to describe the stages of a cyber intrusion and help defenders detect and stop attacks
- Identifies what the adversaries must complete in order to achieve their objective
- Helps analysts understand where in the attack lifecycle they can detect or stop an adversary

Ref:
- https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html

|Phase | What the attacker is doing |
|---------|---------------------------|
| 1. **Reconnaissance** | Gathering information on the target (OSINT, scanning, email harvesting) |
| 2. **Weaponization** | Creating the payload (malware, exploit/dropper) |
| 3. **Delivery** | Sending the weapon (phishing email, malicious USB, watering hole, etc) |
| 4. **Exploitation** | Exploiting the vulnerability (code executes on the target system) |
| 5. **Installation** | Installing malware and establishing persistence (backdoor, rootkit, etc) |
| 6. **Command & Control (C2)** | Attacker establishes remote channel back to compromised host |
| 7. **Actions on Objectives** | Attacker does what they came to do (exfil/destroy data, ransomware) |


# MITRE ATT&CK Matrix

Organizes attacker behavior into tactics, techniques, and procedures
- Based on observed cyberattacks rather than theory
- Helps defenders detect, analyze, and respond to threats
- Used by governments, private sector, and cybersecurity vendors

Ref:
- https://attack.mitre.org/

|Tactic|What the attacker is doing|
|---------|--------------------------|
|**Reconnaissance**|Attempting to gather information they can use to plan future operations|
|**Resource Development**|Trying to establish resources they can use to support operations|
|**Initial Access**|Trying to get into your network|
|**Execution**|Trying to run malicious code|
|**Persistence**|Trying to maintain their foothold|
|**Privilege Escalation**|Trying to gain higher-level permissions|
|**Stealth**|Trying to hide and conceal their actions, appearing as normal behavior|
|**Defense Impairment**|Trying to break security mechanisms, pipelines, and tooling so defenders can’t see or trust what’s happening|
|**Credential Access**|Trying to steal account names and passwords|
|**Discovery**|Trying to figure out your environment|
|**Lateral Movement**|Trying to move through your environment|
|**Collection**|Trying to gather data of interest to their goal|
|**Command and Control**|Trying to communicate with compromised systems to control them|
|**Exfiltration**|Trying to steal data|
|**Impact**|Trying to manipulate, interrupt, or destroy your systems and data|


# OWASP Top 10 (2025)

Open Web Application Security Project
- The OWASP Top 10 is a standard awareness document for developers and web application security. It represents a broad consensus about the most critical security risks to web applications.

Ref:
- https://owasp.org/Top10/2025/


| # | Category | What it do |
|----|----|----|------------|
|A01| Broken Access Control | When a user acts outside of their intended permissions |
|A02| Security Misconfiguration | When a system, application, or cloud service is set up incorrectly from a security perspective | 
|A03| Software Supply Chain Failures | Breakdowns or other compromises in the process of building, distributing, or updating software |
|A04| Cryptographic Failures | Failures related to the lack of cryptography, insufficiently strong cryptography, leaking of cryptographic keys, and related errors |
|A05| Injection | Application flaw that allows untrusted user input to be sent to an interpreter and causes the interpreter to execute parts of that input as commands |
|A06| Insecure Design | Broad category representing different weaknesses, expressed as “missing or ineffective control design" |
|A07| Authentication Failures | When an attacker is able to trick a system into recognizing an invalid or incorrect user as legitimate |
|A08| Software or Data Integrity Failures | Code and infrastructure that does not protect against invalid or untrusted code or data being treated as trusted and valid |
|A09| Security Logging and Alerting Failures | Without logging and monitoring, attacks and breaches cannot be detected, and without alerting it is very difficult to respond quickly and effectively during a security incident |
|A10| Mishandling of Exceptional Conditions | When programs fail to prevent, detect, and respond to unusual and unpredictable situations, which leads to crashes, unexpected behavior, and sometimes vulnerabilities |

# Threat Intelligence

The process of collecting, analyzing, and sharing information about threats to help defenders make better decisions
- Understanding who is attacking, how, and what to do about it

These are just a few sources:

| Source | What it covers |
|--------|---------------|
| MITRE ATT&CK | TTPs based on observed attacks |
| CISA Advisories | US gov alerts on active threats, vulnerabilities, and mitigations |
| VirusTotal | Url/IP/domain/file scanning for community sources threat scanning |
| Shodan | A search engine for internet connected devices (scanning/banner collection/vulns) |

Refs:
- https://www.cisa.gov/
- https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-209a
- https://www.virustotal.com/
- https://www.shodan.io/

# Vulnerability Research

Finding, analyzing, and documenting security flaws in software and systems
- Discover vulnerabilities before attackers do, or understand ones already being exploited
- Pretty much always the next step after initial scanning/enumeration/footprinting
- How would you know what to target?

|Source| What it be|
|----|----|
|Common Vulnerabilities and Exposures|Catalog of publicly disclosed vulnerabilities (like [CVE - Log4j](https://www.cve.org/CVERecord?id=CVE-2021-44228))|
|National Vulnerability Database| NIST's CVE database with CVSS severity scores (like [NVD - Log4j](https://nvd.nist.gov/vuln/detail/CVE-2021-44228))|
|Common Vulnerability Scoring System|A way to capture the principal characteristics of a vulnerability and produce a numerical score reflecting its severity|
|Common Configuration Enumeration|IDs for system misconfigurations|
|Common Weakness Enumeration|A community-developed list of common software and hardware weakness types|

Refs:
- https://www.cve.org/
- https://nvd.nist.gov/
- https://www.first.org/cvss/
- https://cce.mitre.org/
- https://cwe.mitre.org/


# Notes

- Cyber Kill Chain explains **when** an attack occurs
- MITRE ATT&CK explains **what** the attacker is doing
- CVE/NVD/CISA explain **which vulnerabilities** attackers are exploiting
- Vendor advisories and CCE explain **how to mitigate** those vulnerabilities