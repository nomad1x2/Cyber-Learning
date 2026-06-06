# Python Virtual Environments

## Overview

The venv module supports creating lightweight “virtual environments”, each with their own independent set of Python packages installed in their site directories. A virtual environment is created on top of an existing Python installation, known as the virtual environment’s “base” Python, and by default is isolated from the packages in the base environment, so that only those explicitly installed in the virtual environment are available. See Virtual Environments and site’s virtual environments documentation for more information.
Ref:
- https://docs.python.org/3/library/venv.html

Essentially, a virtual environment is good to use for different projects depending on the python packages needed for that specific project. Some packages may conflict with others which could cause issues. For example, if a project was built with `Package v1.2` in mind and not yet optimized for `Package v2.1`, then that project may not run properly on an environment with the `v2.1` project.



---

## Commands / Steps

```bash
# Create the virtual environment
python3 -m venv myenv

# Activate it
source myenv/bin/activate

# install necessary packages
pip install requests numpy

# Save dependencies for that project
pip freeze > requirements.txt

# Install the environment somewhere else
pip install -r requirements.txt

# deactivate the venv when finished
deactivate
```

## Example:

```bash
┌──(nomad㉿nomad)-[~]
└─$ python3 -m venv venv-proj

┌──(nomad㉿nomad)-[~]
└─$ ls venv-proj/
bin  include  lib  lib64  pyvenv.cfg

┌──(nomad㉿nomad)-[~]
└─$ source venv-proj/bin/activate

┌──(venv-proj)(nomad㉿nomad)-[~]
└─$ pip install pwn Crypto

┌──(venv-proj)(nomad㉿nomad)-[~]
└─$ pip freeze > requirements.txt

┌──(venv-proj)(nomad㉿nomad)-[~]
└─$ cat requirements.txt
bcrypt==5.0.0
capstone==6.0.0a9
certifi==2026.5.20
cffi==2.0.0
charset-normalizer==3.4.7
colored-traceback==0.4.2
crypto==1.4.1
cryptography==48.0.0
idna==3.18
intervaltree==3.2.1
invoke==3.0.3
Mako==1.3.12
MarkupSafe==3.0.3
Naked==0.1.32
packaging==26.2
paramiko==5.0.0
plumbum==2.0.0
psutil==7.2.2
pwn==1.0
pwntools==4.15.0
pycparser==3.0
pyelftools==0.33
Pygments==2.20.0
PyNaCl==1.6.2
pyserial==3.5
PySocks==1.7.1
python-dateutil==2.9.0.post0
PyYAML==6.0.3
requests==2.34.2
ROPGadget==7.7
rpyc==6.0.2
shellescape==3.8.1
six==1.17.0
sortedcontainers==2.4.0
unicorn==2.1.2
unix-ar==0.2.1
urllib3==2.7.0
zstandard==0.25.0

┌──(venv-proj)(nomad㉿nomad)-[~]
└─$ deactivate

┌──(nomad㉿nomad)-[~]
└─$ python3 -m venv venv-proj-new

┌──(nomad㉿nomad)-[~]
└─$ source venv-proj-new/bin/activate

┌──(venv-proj-new)(nomad㉿nomad)-[~]
└─$ pip install -r requirements.txt
Collecting bcrypt==5.0.0 (from -r requirements.txt (line 1))
......
Collecting Naked==0.1.32 (from -r requirements.txt (line 14))
......
Successfully installed Mako-1.3.12 MarkupSafe-3.0.3 Naked-0.1.32 PyNaCl-1.6.2 PySocks-1.7.1 PyYAML-6.0.3 Pygments-2.20.0 ROPGadget-7.7 bcrypt-5.0.0 capstone-6.0.0a9 certifi-2026.5.20 cffi-2.0.0 charset-normalizer-3.4.7 colored-traceback-0.4.2 crypto-1.4.1 cryptography-48.0.0 idna-3.18 intervaltree-3.2.1 invoke-3.0.3 packaging-26.2 paramiko-5.0.0 plumbum-2.0.0 psutil-7.2.2 pwn-1.0 pwntools-4.15.0 pycparser-3.0 pyelftools-0.33 pyserial-3.5 python-dateutil-2.9.0.post0 requests-2.34.2 rpyc-6.0.2 shellescape-3.8.1 six-1.17.0 sortedcontainers-2.4.0 unicorn-2.1.2 unix-ar-0.2.1 urllib3-2.7.0 zstandard-0.25.0
```
