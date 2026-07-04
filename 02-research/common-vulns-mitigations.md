# Common Vulnerabilities/Exploits

## Memory Corruption

| Vulnerability | What it means-ish |
|--------------|-----------|
| [Buffer overflow](https://www.cloudflare.com/learning/security/threats/buffer-overflow/) | When a program writing data to a buffer overloads that buffer's capacity (crashes, overwrite return addresses, code execution, information disclosure) |
| [Stack overflow](https://cwe.mitre.org/data/definitions/121.html) | Buffer being overwritten is allocated on the call stack |
| [Heap overflow](https://cwe.mitre.org/data/definitions/122.html) | Buffer that can be overwritten is allocated in the heap portion of memory, generally meaning that the buffer was allocated using a routine such as malloc() |
| [Use after free](https://cwe.mitre.org/data/definitions/416.html) | Program uses a pointer after the memory it points to has been freed |
| [Off by one](https://cwe.mitre.org/data/definitions/193.html) | Uses an incorrect maximum or minimum value that is 1 more, or 1 less, than the correct value |

## Injections

| Vulnerability | What the attacker be doing |
|--------------|-----------|
| [SQL injection (SQLi)](https://cwe.mitre.org/data/definitions/89.html) | Attacker injects SQL into an input field (can read, modify, delete database data) |
| [Command injection](https://cwe.mitre.org/data/definitions/77.html) | Attacker injects commands into input that get executed by the target |
| [Cross site Scripting](https://cwe.mitre.org/data/definitions/79.html) | Attacker injects malicious scripts into a page viewed by other users |
| [Deserialization](https://cwe.mitre.org/data/definitions/502.html) | App deserializes untrusted data |
| [LDAP injection](https://cwe.mitre.org/data/definitions/90.html) | Attacker injects LDAP statements into an input used in directory queries — bypass auth, extract user data |
| [Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html) | Forces server to make requests to unintended internal/external locations |
| [Path traversal](https://cwe.mitre.org/data/definitions/22.html) | Attacker uses `../` sequences to access files outside the intended directory |

## Logic / Design Flaws

| Vulnerability | What be happening |
|--------------|-----------|
|Broken access control|App fails to enforce what users are allowed to do |
|Security misconfiguration| Default creds, unnecessary services, verbose errors, open storage buckets |
|Vulnerable components| Using libraries/frameworks with known unpatched CVEs |
| [Race condition](https://cwe.mitre.org/data/definitions/362.html) | Two processes access shared resource simultaneously (attacker exploits the window between check and use (TOCTOU)) |
| [Cryptographic failures](https://cwe.mitre.org/data/definitions/327.html) | Weak/broken algorithms, hardcoded keys, improper certificate validation |

## Top Routinely Exploited Vulnerabilities (2023)

CISA-AA24-317A

- CVEs routinely and frequently exploited by malicious cyber actors in 2023 and their associated CWEs
- "In 2023, the majority of the most frequently exploited vulnerabilities were initially exploited as a zero-day, which is an increase from 2022, when less than half of the top exploited vulnerabilities were exploited as a zero-day"

| CVE | Vendor | Vulnerability | Description |
|-----|--------|------|------------|
|CVE-2023-3519|Citrix|Code Injection|Allows an unauthenticated user to cause a stack buffer overflow in the NSPPE process by using a HTTP GET request|
|CVE-2023-4966|Citrix|Buffer Overflow|Allows session token leakage; a proof-of-concept for this exploit was revealed in October 2023|
|CVE-2023-20198|Cisco|Privilege Escalation|Allows unauthorized users to gain initial access and issue a command to create a local user and password combination, resulting in the ability to log in with normal user access|
|CVE-2023-20273|Cisco|Web UI Command Injection|Allows privilege escalation, once a local user has been created, to root privileges|
|CVE-2023-27997|Fortinet|Heap-Based Buffer Overflow|Allows a remote user to craft specific requests to execute arbitrary code or commands|
|CVE-2023-34362|Progress|SQL Injection|Allows a malicious cyber actor to obtain remote code execution via this access by abusing a deserialization call|
|CVE-2023-22515|Atlassian|Broken Access Control|The exploit creates a new administrator user and uploads a malicious plugin to get arbitrary code execution|
|CVE-2021-44228|Apache|Remote Code Execution|**Log4j always being a problem** -- An actor can exploit this vulnerability by submitting a specially crafted request to a vulnerable system, causing the execution of arbitrary code|
|CVE-2023-2868|Barracuda Networks|Improper Input Validation|Allows an individual to obtain unauthorized access and remotely execute system commands via the ESG appliance|
|CVE-2022-47966|Zoho|Remote Code Execution|Allows an unauthenticated user to execute arbitrary code by providing a crafted samlResponse XML to the ServiceDesk Plus SAML endpoint|
|CVE-2023-27350|PaperCut|Improper Access Control|Allows a malicious cyber actor to chain an authentication bypass vulnerability with the abuse of built-in scripting functionality to execute code|
|CVE-2020-1472|Microsoft|Privilege Escalation|An unauthorized user may use non-default configurations to establish a vulnerable Netlogon secure channel connection to a domain controller by using the Netlogon Remote Protocol (included in top routinely exploited vulnerabilities lists since 2021)|
|CVE-2023-42793|JetBrains|Authentication Bypass|Allows authentication bypass that allows remote code execution against vulnerable JetBrains TeamCity servers|
|CVE-2023-23397|Microsoft|Privilege Escalation|A threat actor can send a specially crafted email that the Outlook client will automatically trigger when Outlook processes it|
|CVE-2023-49103|ownCloud|Information Disclosure|An unauthenticated user can access sensitive data such as admin passwords, mail server credentials, and license keys|

Attackers usually favor older known CVEs because they are easy to exploit and systems remain unpatched
- Something something n-day
- Patching is the single most effective mitigation

Ref:
- https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-317a

## Mitigations

Vendors/developers:
- Identify repeatedly exploited classes of vulnerability
- Follow [SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final)
  - Secure Software Development Framework (SSDF) - Recommendations for Mitigating the Risk of Software Vulnerabilities
- Configure production-ready products to have the most secure settings by default
- Ensure published CVEs include the proper CWE field

End users/organizations:
- Update software, operating systems, applications, and firmware on IT network assets in a timely manner
- Routinely perform automated asset discovery
- Implement a robust patch management process/central patch management
- Perform regular secure system backups/known good copies
- Maintain an updated cybersecurity incident response plan

Identity/access management:
- Enforce phishing-resistant multifactor authentication (MFA) for all users
- Regularly review, validate, or remove unprivileged accounts
- Configure access control under the principle of least privilege

Protective controls/architecture
- Properly configure and secure internet-facing network devices
- Implement Zero Trust Network Architecture (ZTNA)
- Continuously monitor the attack surface

Supply chain security:
- Reduce third-party applications and unique system/application builds
- Ask your software providers to discuss their secure by design program

# Notes

- MITRE ATT&CK / OWASP Top 10/ using google -- all good ways to research vulnerabilities
  - most of the time, pre coded exploits are easy to locate

- [MITRE ATT&CK/OWASP/Threat intel writeups](vuln-research-intel.md)