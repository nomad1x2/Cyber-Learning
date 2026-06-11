# SCP (Secure Copy Protocol)

## Overview

Copies files between hosts over SSH; uses same authentication and encryption as SSH
- Syntax is always `scp [flags] SOURCE DESTINATION`, where remote paths are written as `host:path`.

---

## Commands / Steps

```bash
# Create a test file (im just re-enforcing python hashlib)
python3 -c "import hashlib; print(hashlib.md5(b'scp test').hexdigest())" > scp-test.txt

# Kali to remote host
scp scp-test.txt ubuntu:~/scp-test/

# Remote host to kali (pull from kali)
scp ubuntu:~/scp-test/scp-test.txt ./rx-scp-test.txt

# Entire directory (-r recursive)
scp -r ~/scp ubuntu:~/scp-test/dir-test

# Non standard port (-P)
scp -P 2222 ./* pi-jump:~/

# IPv6 (pi ll address must be wrapped in brackets, local machine interface after the % (egress int))
scp -6 -r ../scp pi@'[fe80::ba27:ebff:feb1:a%eth0]':~/
```

| Flag | Description |
|---|---|
| `-r` | Recursive - copy entire directory |
| `-P` | Specify port (uppercase, unlike ssh which is lowercase) |
| `-6` | Force IPv6 |
| `-i` | Specify identity file |
| `-v` | Verbose output |

---

## Screenshots
![scp kali to ubuntu](../../assets/screenshots/linux/scp1.png)
![scp ubuntu to kali](../../assets/screenshots/linux/scp2.png)
![scp directory](../../assets/screenshots/linux/scp3.png)
![scp non-standard port](../../assets/screenshots/linux/scp4.png)
![scp ipv6](../../assets/screenshots/linux/scp5.png)

---

## Notes / Gotchas
- IPv6 addresses must be wrapped in brackets: `'[fe80::...%eth0]'` and identify the egress int (%eth0 for our local machine)
- SCP uses our SSH config - `scp ubuntu:~/file .` works because `ubuntu` is defined in `~/.ssh/config` with ProxyJump, so it routes through the Pi automatically
- `scp -r` copies the directory itself, not just its contents - destination will have the folder name appended