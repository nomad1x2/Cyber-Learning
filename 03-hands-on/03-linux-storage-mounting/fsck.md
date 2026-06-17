
# fsck (Filesystem Check)

## Overview

fsck checks and repairs Linux filesystems.
- Should only be run on unmounted filesystems; running on a mounted filesystem can cause corruption
- Runs automatically on boot if the filesystem was not cleanly unmounted

Ref:
- https://linuxhandbook.com/fsck-command/

---

## Commands / Steps


```bash
# Check a filesystem
sudo fsck /dev/sdb1

# Check and auto-repair without prompting
sudo fsck -y /dev/sdb1

# Check all filesystems in fstab
sudo fsck -A

# Force check even if filesystem appears clean
sudo fsck -f /dev/sdb1

# Check specific filesystem type
sudo fsck -t ext4 /dev/sdb1
```

**Output:**

```
fsck from util-linux 2.42
e2fsck 1.47.4 (6-Mar-2025)
/dev/sdb1: clean, 12/327680 files, 42397/1310464 blocks
```
- `clean` - no errors found
- `files` - inodes used vs total
- `blocks` - blocks used vs total

**If errors are found:**

```
/dev/sdb1: UNEXPECTED INCONSISTENCY; RUN fsck MANUALLY

```
Run `sudo fsck -y /dev/sdb1` to repair

| Flag | Description |
|---|---|
| `-y` | Auto-answer yes to all repair prompts |
| `-n` | Check only, no repairs |
| `-f` | Force check even if marked clean |
| `-A` | Check all filesystems in /etc/fstab |
| `-t` | Specify filesystem type |

---

## Notes / Gotchas
- **Never run fsck on a mounted filesystem**, unmount first or boot into recovery mode
- fsck is called automatically on boot after unclean shutdown; the pass number in fstab (last column) controls the order it runs
- Pass `0` = skip fsck, `1` = check first (root), `2` = check after root
- For ext4 use `e2fsck` directly for more options: `sudo e2fsck -f /dev/sdb1`
