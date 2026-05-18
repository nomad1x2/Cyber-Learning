# Secure Shell

## Setting simple SSH on a fresh Ubuntu boot:
- sudo apt install openssh-server -y
- sudo systemctl start ssh
- sudp systemctl status ssh

## SCP from my WSL instance running on my Windows/Kali host:
- scp nomad@192.168.8.108:/home/nomad/Desktop/ssh_setup.png ./

![WSL scp](../../../05-assets/images/scp_1.png)

![Ubuntu ssh](../../../05-assets/images/ssh_setup.png)
