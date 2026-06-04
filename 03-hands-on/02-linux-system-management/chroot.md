# chroot

Pulling this from the man pages:

```bash
man chroot

NAME
      chroot - run command or interactive shell with special root directory
DESCRIPTION
      Run COMMAND with root directory set to NEWROOT.
      If no command is given, run '"$SHELL" -i' (default: '/bin/sh -i').
```

A chroot is an operation that changes the apparent root directory for the current running process and their children. A program that is run in such a modified environment cannot access files and commands outside the specified directory tree. This modified environment is called a _chroot jail_. The main use case is isolating daemons so that vulnerabilities are contained to that process. For example, Postfix can be configured to run inside a chroot with limited directory access, so any bug found affects only Postfix and nothing else.
Changing root is also commonly done for system maintenance when booting or logging in is no longer possible:

- Reinstalling the boot loader
- Rebuilding the initramfs image
- Upgrading or downgrading packages
- Resetting a forgotten password
- Building packages in a clean environment

Refs:
- https://wiki.archlinux.org/title/Chroot
- https://www.howtogeek.com/devops/what-is-chroot-on-linux-and-how-do-you-use-it/

---

## Commands / Steps

Simulated fake root:
```bash
┌──(nomad㉿nomad)-[~/testroot]
└─$ tree
.
├── bin
│   ├── bash
│   ├── cat
│   ├── echo
│   ├── ls
│   ├── mkdir
│   ├── pwd
│   ├── rm
│   └── touch
├── etc
│   ├── hostname
│   └── passwd
├── home
├── lib
│   └── x86_64-linux-gnu
├── lib64
│   └── ld-linux-x86-64.so.2
├── root
├── tmp
└── usr
    └── lib
        └── x86_64-linux-gnu
            ├── libcap.so.2
            ├── libc.so.6
            ├── libpcre2-8.so.0
            ├── libselinux.so.1
            └── libtinfo.so.6

12 directories, 16 files
```

Chroot jail:
```bash
┌──(nomad㉿nomad)-[~/testroot]
└─$ pwd
/home/nomad/testroot

┌──(nomad㉿nomad)-[~/testroot]
└─$ sudo chroot ~/testroot /bin/bash
bash-5.3# pwd
/
bash-5.3#
```

Proof of concept:
```bash
# What does / look like?
bash-5.3# ls /
bin  etc  home  lib  lib64  root  tmp  usr

# Can we see your real home?
bash-5.3# ls /home/nomad
ls: cannot access '/home/nomad': No such file or directory # no

# Fake hostname
bash-5.3# cat /etc/hostname
testroot-machine

# Create a file inside
bash-5.3# touch /tmp/testfile
bash-5.3# ls /tmp
testfile

# Exit and verify the file exists on real fs
bash-5.3# exit
┌──(nomad㉿nomad)-[~/testroot]
└─$ ls ./tmp
testfile    # testfile is there; chroot writes go to testroot/
```

---

## Notes / Gotchas

- Not true containerization; root can escape chroot, it's not a real security boundary
- Writes inside the jail write on the real filesystem under the chroot directory
- Use when: system won't boot, testing destructive changes, running legacy binaries with specific lib layouts