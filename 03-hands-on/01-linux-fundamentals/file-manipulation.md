# File & Directory Manipulation

## find

search for files in a directory hierarchy

```bash
# Find a file by name
find / -name "example.txt"

# Find files modified in the last 24 hours
find /var -mtime -1

# Find symbolic links (-type l) and ignore errors
find / -type l 2>/dev/null

#Find files by exact permissions (404), exact size in bytes (333c), and name exactly 14 characters in length (14 question marks = 14 characters)
find /path -perm 404 -size 333c -name ??????????????
```

_Could also pipe into grep for more regex_

---

## cp

copy files and directories

```bash
# Copy a file
cp file.txt /destination/

# Copy a directory recursively
cp -r /source/ /destination/
```

---

## locate

find files by name, quickly
- Needs a current indexed file database (run `updatedb`) before locate will find newly created files

```bash
# simple locate
locate /example.txt

# only match basename
locate -b /example.txt

# case insensitive
locate -i example.txt 

# regex
locate -r example.txt

# extended regex
locate --regex example.txt 
```

---

## grep

print lines that match patterns

```bash
# Search for a string in a file
grep "error" /file.txt

# Search for a string recursively in a dir
grep -R "error" /Directory

# Search with regex
grep -E "p[a]t{1,2}eRn" /file.txt

# Search case insensitively
grep -i "pAtTeRn" /file.txt

# Invert/omit a pattern in a search
grep -v "grep" /file.txt

# Search and show line number 
grep -n "pattern" /file.txt

# Count the number of matching lines instead of printing them 
grep -c "pattern" /file.txt

#Print only the filenames that contain a match
grep -l "pattern" /directory/*

#Print 3 lines before and after each match (or A/B for after/before)
grep -C 3 "pattern" /file.txt
```

---

## dd

convert and copy a file
- normally use `cp` to copy files/directories unless needing granular byte control 

```bash
# Disk/partition imaging; create a raw byte-for-byte backup
dd if=/dev/sda of=/backup/sda.img bs=4M status=progress

# Clone one disk directly to another
dd if=/dev/sda of=/dev/sdb bs=4M

# Create a bootable USB from an ISO
dd if=image.iso of=/dev/sdb conv=fsync

# Create a file of exact size (100MB of zeros)
dd if=/dev/zero of=empty.img bs=1M count=100

# Skip bytes - read starting at an offset (skip first 2 blocks)
dd if=/dev/sda of=output.img bs=512 skip=2

# Convert a file to uppercase (conv= has misc text transforms too)
dd if=input.txt of=output.txt conv=ucase

# Wipe a drive by overwriting with zeros
dd if=/dev/zero of=/dev/sdb bs=1M status=progress

# Wipe a drive with random data
dd if=/dev/urandom of=/dev/sdb bs=1M status=progress
```

| Option | Description |
|--------|-------------|
| `if=` | Input file (or device) |
| `of=` | Output file (or device) |
| `bs=` | Block size (`512`, `4M`, `1K`, etc) |
| `count=` | Number of blocks to copy |
| `skip=` | Blocks to skip on input |
| `seek=` | Blocks to skip on output |
| `conv=ucase | lcase` | Convert text to upper/lowercase |
| `conv=noerror` | Continue on read errors; useful for damaged disk recovery |
| `conv=fsync` | Flush write cache to hardware before exit; important for USB imaging |
| `conv=swab` | Swap every pair of bytes (endianness fix) |
| `conv=notrunc` | Don't truncate output; preserves data beyond what dd writes |
| `status=progress` | Show live progress and speed |

_Need to be careful, `dd` will silently overwrite data_

---

## sed

stream editor for filtering and transforming text

```bash
# add "First line" to the first line in file.txt
sed -i '1i First line' file.txt

# replace first match on each line
sed -i 's/old/new/' file

# only print displaying match replacements
sed 's/old/new/g' file

# replace second match
sed -i 's/old/new/2' file

# case-insensitive replace
sed -i 's/old/new/Ig' file

# only print and collapse white space
sed 's/[[:space:]]\+//g' file

# replace using regex
sed -E 's/[old]/new/Ig' file
```

| Option | Description |
|--------|-------------|
|`-i`|Edit in place|
|`-E`|Regex|

Ref:
- https://linuxize.com/cheatsheet/sed/

---

## vim

Vi IMproved, a programmer's text editor

```bash
vim file.txt
```
_Basic vim: `i` to insert (start typing), `ESC` to exit insert (run commands:), `:wq` to save and quit, `:q!` to quit without saving_

---

## RegEx

| Pattern | Description |
|---------|-------------|
| `[a-z]` | Lowercase range, matches any single lowercase letter |
| `[abc]` | Lowercase a, b, or c |
| `[A-Z]` | Uppercase range, matches any single uppercase letter |
| `[0-9]` | Numeric range, matches any single digit from 0 to 9 |
| `[a-zA-Z0-9]` | Alphanumeric, matches any letter or number |
| `[^abc]` | Negation, matches any character NOT in the set |
| `[[:alpha:]]` | Alphabetic, match letters |
| `[[:digit:]]` | Digits, match numbers |
| `[[:punct:]]` | Punctuation, match punctuation characters |
| `[[:space:]]` | Whitespace, match spaces, tabs, newlines |
| `[[:upper:]]` | Uppercase, equivalent of `[A-Z]` |
| `[[:lower:]]` | Lowercase, equivalent of `[a-z]` |
| `[[:alnum:]]` | Alphanumeric, equivalent of `[a-zA-Z0-9]` |
| `?` | Glob wildcard, matches any ONE character |
| `*` | Glob wildcard, matches any number of characters including none |
| `.` | Regex wildcard, matches any single character |
| `+` | Regex, one or more of the preceding character |
| `\|` | Or, `this\|or\|that` matches "this", "or", or "that" |
| `^` | Anchor, matches start of a line |
| `\<` | Anchor, matches start of a word |
| `\>` | Anchor, matches end of a word |
| `$` | Anchor, matches end of a line |
| `\w` | Any word character (alphanumeric + underscore) |
| `\s` | Any whitespace character |
| `\d` | Any digit, same as `[0-9]` |
| `\n` | Newline |
| `\t` | Tab |
| `\{x,y\}` | Repetition, matches the preceding character x to y times |

---

## Screenshots

## Notes / Gotchas