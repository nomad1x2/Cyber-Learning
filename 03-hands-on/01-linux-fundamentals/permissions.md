# File Permissions (chmod & chown)

Breaking down file permissions (octal/symbolic) and other characters, with command examples

## Permission modes
|Octal|Binary|Permissions|
|-----|------|-----------|
0|000|---|
1|001|--x|
2|010|-w-|
3|011|-wx|
4|100|r--|
5|101|r-x|
6|110|rw-|
7|111|rwx|

Permissions are structured as: `[type][user][group][other]`

| Character | Position | Meaning |
|-----------|----------|---------|
| `-` | first character | regular file |
| `d` | first character | directory |
| `l` | first character | symbolic link |
| `s` | user execute bit | SUID set |
| `s` | group execute bit | SGID set |
| `t` | other execute bit | sticky bit set |
| `T` | other execute bit | sticky bit set, but execute NOT set for others|
| `S` | user or group execute bit | SUID/SGID set, but execute NOT set for that user/group|

---

| Mode | Symbolic | Meaning |
|------|----------|---------|
| `0777` | `-rwxrwxrwx` | regular file, full permissions for everyone |
| `0755` | `-rwxr-xr-x` | file; owner can write, group/others can only read and execute |
| `0775` | `drwxrwxr-x` | directory; owner/group can read, write, and execute, others can only read and execute |
| `1755` | `drwxr-xr-t` | sticky bit set, execute IS set for others |
| `1644` | `-rw-r--r-T` | sticky bit set, execute NOT set for others |
| `4755` | `-rwsr-xr-x` | SUID set, execute IS set for owner |
| `4644` | `-rwSr--r--` | SUID set, execute NOT set for owner |
| `2755` | `drwxr-sr-x` | SGID set, execute IS set for group |
| `2744` | `drwxr-Sr--` | SGID set, execute NOT set for group |
---

## Commands / Steps


### chmod - change Permissions

```bash
#Sets permissions in numeric (octal) mode: 7 = rwx for owner, 4 = r-- for group, 4 = r-- for others
chmod 744 /file.txt

# Sets full permissions AND the sticky bit (the leading 1) on a directory
chmod 1777 sticky_dir

# Sets permissions in symbolic mode: explicitly defines read/write/execute for user, group, and others
chmod u=rwx,g=r,o=r /file.txt

# Adds the sticky bit. on a directory, only the file owner can delete their own files even if others have write access
chmod +t /sticky_dir/

# Sets the SUID bit. when executed, the program runs with the permissions of the file owner rather than the user running it
chmod u+s /suid_file

# Sets the SGID bit on a directory. any new files created inside will inherit the directory's group ownership instead of the creator's primary group
chmod g+s /sgid_dir/

# Apply permissions recursively to a directory and everything inside it
chmod -R 755 /directory/
```

### chown - change ownership

```bash
# USER:GROUP
# Sets both the user owner and group owner to user2/group2
sudo chown user2:group2 /sgid_dir

# USER:
# Changes user owner to user1 (group owner defaults to user1's group)
sudo chown user1: /file.txt

# USER
# Changes ONLY user owner to anotheruser
sudo chown anotheruser /file.txt

# :GROUP
# Changes ONLY the group owner to group1
sudo chown :group1 /file.txt

# Apply ownership change recursively to a directory and everything inside it
sudo chown -R user2:group2 /directory/
```

---


## Screenshots


---

## Notes / Gotchas

