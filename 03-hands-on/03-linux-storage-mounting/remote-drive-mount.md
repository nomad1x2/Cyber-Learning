# Mounting a Remote Windows Drive on Linux

Windows shares folders using SMB (port 445). Linux can mount SMB shares using the cifs-utils package (NFS natively)

## Commands / Steps

First use `smbclient -L` to list the shares from a Windows machine using SMB:

```bash
smbclient -L //192.168.8.201 -U User03
```

Then create a mount point and mount the shared folder:

```bash
sudo mkdir -p /mnt/Media_Share
sudo mount //192.168.8.201/Media_Share /mnt/Media_Share -o user=User03
```

- Using `-o user=User03` to specify using the `username` option

Then verify shared folder contents:

```bash
ls /mnt/Media_Share
cat /mnt/Media_Share/New.txt
```

---

Can also make this persistent by adding an entry in `/etc/fstab`

Ref:
- https://linuxvox.com/blog/mount-smb-share-on-linux/

## Screenshots

![win share1](../../assets/images/linux/linux-windows-share1.png)
![win share1](../../assets/images/linux/linux-windows-share2.png)

---

## Notes / Gotchas

_Anything that tripped you up, edge cases, or worth flagging for review._
