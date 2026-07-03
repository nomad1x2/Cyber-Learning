
# Lockheed Martin Cyber Kill Chain

- Framework developed by Lockheed Martin to describe the stages of a cyber intrusion and help defenders detect and stop attacks
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

- Organizes attacker behavior into tactics, techniques, and procedures
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


# OWASP Top 10





# Threat Intelligence




# Vulnerability Research




# Notes

- Cyber Kill Chain explains **when** an attack occurs
- MITRE ATT&CK explains **what** the attacker is doing
- CVE/NVD/CISA explain **which vulnerabilities** attackers are exploiting
- Vendor advisories and CCE explain **how to mitigate** those vulnerabilities