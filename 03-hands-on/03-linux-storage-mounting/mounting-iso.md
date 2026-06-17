
# Mounting ISOs

## Overview

ISOs can be mounted as loop devices without burning them to physical media
- The loop device in Linux provides a mechanism to mount an ISO image as if it were a physical disk partition

Ref:
- https://linuxvox.com/blog/linux-mount-loop-iso/

---

## Commands / Steps

```bash
# Mount a single ISO
sudo mkdir -p /mnt/iso/rocky
sudo mount -o loop Rocky-x86_64-boot.iso /mnt/iso/rocky
```

![mounted1](../../assets/images/linux/mounted1.png)


```bash
# For loop
for iso in ~/fs/*.iso; do sudo mkdir -p /mnt/iso/$(basename "$iso" .iso) && sudo mount -o loop "$iso" /mnt/iso/$(basename "$iso" .iso); done

# Verify all mounted
df -h | grep iso
ls /mnt/iso/

# Unmount all ISOs
for iso in ~/fs/*.iso; do sudo umount /mnt/iso/$(basename "$iso" .iso); done
```

![mounted2](../../assets/images/linux/mounted2.png)


**Loop breakdown:**
```bash
# iterate over every .iso in ~/fs/
for iso in ~/fs/*.iso; do
    sudo mkdir -p /mnt/iso/$(basename "$iso" .iso)  # create mount point named after ISO
    && sudo mount -o loop "$iso" /mnt/iso/$(basename "$iso" .iso) # mount it
done
```

- `basename "$iso" .iso` - strips the path and `.iso` extension leaving just the filename
- `-o loop` - tells mount to use a loop device (required for files)
- `&&` - only mount if mkdir succeeded

---

## Notes / Gotchas
- ISOs are usually mounted read-only by default to not cause unwanted overwrites
  - `WARNING: source write-protected`
- Unmount before removing mount points
  - `sudo umount` then `sudo rmdir`