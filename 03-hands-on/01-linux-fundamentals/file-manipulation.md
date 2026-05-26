# File & Directory Manipulation

## find

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

```bash
# Copy a file
cp file.txt /destination/

# Copy a directory recursively
cp -r /source/ /destination/
```

---

## locate

```bash
# Needs a current indexed file database (run `updatedb`)
# Must be run before locate will find newly created files
locate example.txt
```

---

## grep

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

```bash
# Need to do a little more research for dd
```

---

## vim

```bash
vim file.txt
```
_Basic vim: `i` to insert (start typing), `ESC` to exit insert (run commands:), `:wq` to save and quit, `:q!` to quit without saving_

---
## RegEx

| Pattern | Description |
|---------|-------------|
| `[a-z]` | Lowercase range, matches any single lowercase letter |
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