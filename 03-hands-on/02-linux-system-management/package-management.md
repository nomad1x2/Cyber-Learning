# Package Management (apt, yum, dpkg, rpm, pip)

## Overview

Package managers handle installing, updating, and removing software:
- Debian systems use `apt` and `dpkg`
- Red hat systems use `yum` or `dnf`
- Python uses `pip`

---

## apt (debian high-level)

```bash
# Refresh the package index (what new upgrades can we download)
sudo apt update

# Upgrade those new packages
sudo apt upgrade

# Upgrade and resolve dependency changes
sudo apt full-upgrade

# download AND install
sudo apt install PACKAGE

# remove (maintain config files)
sudo apt remove PACKAGE

# remove (remove config files)
sudo apt purge PACKAGE

# Download only, dont install (no dependencies)
sudo apt download PACKAGE

# Download only, dont install (with dependencies)
sudo apt install --download-only PACKAGE

# search repositories
apt search PACKAGE
```

Repo files live in:
- `/etc/apt/sources.list` - main sources file
- `/etc/apt/sources.list.d/` - additional repository definition files (`.list` or `.sources`)

Ref:
- https://linuxvox.com/blog/ubuntu-apt-repository/

---

## dpkg (debian low-level)

`apt` is a essentially the frontend for `dpkg`. Use `dpkg` directly when working with `.deb` files

```bash
# install a .deb file
dpkg -i PACKAGE.deb  

# remove (keep config files)
dpkg -r PACKAGE     

# purge (removes config files)      
dpkg -P PACKAGE

# display package information
dpkg -p PACKAGE   

# list all installed packages
dpkg -l

# list files installed by a package
dpkg -L PACKAGE

# extract contents of a .deb without installing
dpkg -x PACKAGE.deb ./
```

Ref:
- https://www.digitalocean.com/community/tutorials/dpkg-command-in-linux

---

## yum / dnf (RHEL high-level)

`dnf` is the modern replacement for `yum`

```bash
# update package metadata and packages
sudo dnf/yum update

# install package
sudo dnf/yum install PACKAGE

# search repositories
dnf/yum search PACKAGE
```

Repo files live in:
- `/etc/yum.conf` - global config
- `/etc/yum.repos.d/` - individual `.repo` files per repository

Ref
- https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sec-configuring_yum_and_yum_repositories

---

## rpm (RHEL low-level)

Similar to dpkg but for `.rpm` files.

```bash
# install a .rpm package
rpm -i PACKAGE.rpm

# upgrade package
rpm -U PACKAGE.rpm

# remove
rpm -e PACKAGE

# list all installed packages
rpm -qa

# list files installed by a package
rpm -ql PACKAGE

# query installed package
rpm -q PACKAGE
```

Ref:
- https://linuxvox.com/blog/linux-what-is-rpm/
- https://www.geeksforgeeks.org/linux-unix/how-to-use-the-rpm-command-in-linux/

---

## pip (python)

```bash
# install python package
pip install PACKAGE

# install specific package ver
pip install PACKAGE==#.#.#

# install dependencies listed in a req file
pip install -r requirements.txt

# show installed packages
pip list

# show package information
pip show PACKAGE
```

---

## .whl (wheel)

A wheel (`.whl`) is a pre-built Python package that can be installed directly without compiling source code
- Contains package files and installation metadata
- Stored as a `.zip` archive

```bash
pip install package.whl
```

Ref:
- https://packaging.python.org/en/latest/specifications/binary-distribution-format/

---

## Notes / Gotchas
- Always run `apt update` before `apt upgrade`
- `apt remove` leaves config files behind; `apt purge` removes everything
- `dpkg -i` won't resolve dependencies - if it fails with dependency errors, run `sudo apt install -f` afterward to fix them
- `.deb` = Debian/Ubuntu, `.rpm` = RHEL/CentOS
- Some systems wont let you install python packages globally
  - use a virtual environment (`python -m venv`)
  - or force with `--break-system-packages` if you have to