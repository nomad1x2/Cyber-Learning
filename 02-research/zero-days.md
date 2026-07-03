# Zero Day Exploits

- A zero day is a vulnerability that is unknown to the vendor meaning there are zero days of warning to patch it
- No patch exists at time of discovery or exploitation

## Vulnerability Timeline

- Developers create software containing an unknown vulnerability
- Attacker discovers the flaw before the vendor does or acts on it before a patch is written
- Attacker writes and deploys exploit code while the vulnerability is still open
- Developer writes a patch, once applied, no longer called a zero day
  - Called an `n-day`, that "targets a known software vulnerability after it has been publicly disclosed. Attackers leverage the period when patches or mitigations exist but are not yet widely applied."
  - Ref: https://www.windows-active-directory.com/what-is-n-day-exploit.html
- Can go undetected for not just days but months or years

## Key Terms

| Term | What it means |
|------|--------------|
| Zero day vulnerability | The flaw itself, unknown to the vendor |
| Zero day exploit | Code that exploits the vulnerability |
| Zero day attack | Active use of the exploit in the wild |
| N-day | Vulnerability is now public, patch exists but unpatched systems still exposed |
| CVE | Common Vulnerabilities and Exposures - public ID assigned after disclosure |

## Bigly Examples

| Exploit | Year | What it did |
|---------|------|------------|
| Stuxnet | 2010 | Used 4 zero days simultaneously - targeted Iranian nuclear centrifuges |
| EternalBlue (MS17-010) | 2017 | Windows-SMB zero day leaked by `Shadow Brokers` - used in WannaCry ransomware |
| Log4Shell (CVE-2021-44228) | 2021 | zero day in Log4j - affected millions of Java apps |
| SUNBURST | 2020 | SolarWinds supply chain attack - zero day in update mechanism |

## Detection / Defense

- zero days are hard to detect because no signature exists yet
- Defense relies on behavior based detection rather than known signatures

| Strategy | How it helps |
|----------|-------------|
| Behavior based detection | Flag anomalous activity, not known signatures |
| Network segmentation | Limit targets exposd if exploited |
| Patch management | Reduces N-day exposure window |
| Threat intel | Early warnings |
| Zero trust architecture | Always assume breach - limits lateral movement |

Ref:
- https://cloud.google.com/security/resources/insights/what-zero-day-exploit
- https://en.wikipedia.org/wiki/Stuxnet
- https://en.wikipedia.org/wiki/EternalBlue
- https://en.wikipedia.org/wiki/Log4Shell
- https://en.wikipedia.org/wiki/SolarWinds#SUNBURST