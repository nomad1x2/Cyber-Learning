# Compression & Encryption Tools


## Overview

| Utility |Description                                                                                                            |
|---------|-----------------------------------------------------------------------------------------------------------------------|
| tar     | Archiving program designed to store multiple files in a single file, and to manipulate such archives  |
| zip     | Compression and file packaging utility for Unix, VMS, MSDOS, OS/2, Windows 9x/NT/XP, Minix, Atari, Macintosh, Amiga, and Acorn RISC OS (compatible with PKZIP) |
| 7zip    | File archiver with a high compression ratio |
| xz      | General-purpose data compression tool with command line syntax similar to gzip and bzip2 |
| gzip    | The gzip command reduces the size of the named files using Lempel-Ziv coding |
| bzip2   | compresses  files using the Burrows-Wheeler block sorting text compression algorithm, and Huffman coding |

---

## tar

```bash
# Create `file_archive.tar` from file1.dat and file2.dat
tar -cf file_archive.tar file1.dat file2.dat

# List contents of `file_archive.tar` (verbose)
tar -tvf file_archive.tar file1.dat file2.dat

# Extract contents of `file_archive.tar` (verbose)
tar -xf file_archive.tar

# Append file3.dat to `file_archive.tar`
tar -rf file_archive.tar file3.dat
```

| Flag | Description |
|------|-------------|
| `-c` | Create a new archive |
| `-x` | Extract files |
| `-t` | List contents |
| `-r` | Append files to existing archive |
| `-f` | Specify archive file |
| `-v` | Verbose output |
| `-z` | Compress with gzip (`.tar.gz`) |
| `-j` | Compress with bzip2 (`.tar.bz2`) |
| `-J` | Compress with xz (`.tar.xz`) |
| `-C` | Extract to a specific directory |
| `-p` | Preserve permissions |

---

## zip

```bash
# Create/append into `archive.zip` from file1.dat and file2.dat
zip archive.zip file1.dat file2.dat

# Create zip from directory
zip -r archive.zip /file_dir

# Create encrypted zip
zip -e archive.zip file1.dat file2.dat

# Extract contents of `archive.zip`
unzip archive.zip

# List contents of `archive.zip`
unzip -l archive.zip

# Extract contents of `archive.zip`
unzip archive.zip -d /destination
```

| Flag | Description |
|------|-------------|
| `-r` | Recurse into directories |
| `-e` | Encrypt with password |
| `-l` | List contents (unzip) |
| `-d` | Extract to specific directory (unzip) |
| `-1 | -9` | Compression level |

---

## 7zip

```bash
# Create/append into `archive.7z` from file1.dat and file2.dat
7z a archive.7z file1.dat file2.dat

# Extract contents of `archive.7z` (preserves paths)
7z x archive.7z

# Extract contents of `archive.7z` (flat, no paths)
7z e archive.7z

# List contents of `archive.7z`
7z l archive.7z

# Create/append into encrypted `archive.7z` from file1.dat and file2.dat
7z a -pPASSWORD archive.7z file1.dat file2.dat
```

| Flag | Description |
|------|-------------|
| `a` | Add/create archive |
| `x` | Extract preserving paths |
| `e` | Extract flat (no directory structure) |
| `l` | List contents |
| `-p` | Set password |
| `-mx=1 | -mx=9` | Compression level |

---

## xz

```bash
# Compress file in-place (adds .xz extension)
xz big_file.dat 

# Compress file in-place, maintain original
xz -k big_file.dat

# Decompress file in-place
xz -d big_file.dat.xz

# List compression info
xz -l big_file.dat.xz
```

| Flag | Description |
|------|-------------|
| `-d` | Decompress |
| `-k` | Keep original |
| `-v` | Verbose output |
| `-1 | -9` | Compression level (1=fast, 9=best) |

---

## gzip

```bash
# Compress file in-place (adds .gz extension)
gzip big_file.dat 

# Compress file in-place, maintain original
gzip -k big_file.dat

# Decompress file in-place (gunzip)
gzip -d big_file.dat.gz

# List compression info
gzip -l big_file.dat.gz
```

| Flag | Description |
|------|-------------|
| `-d` | Decompress |
| `-k` | Keep original |
| `-l` | List compression info |
| `-r` | Recursively compress dir |
| `-1 | -9` | Compression level (1=fast, 9=best) |

---

## bzip2

```bash
# Compress file in-place (adds .bz2 extension)
bzip2 big_file.dat 

# Compress file in-place, maintain original
bzip2 -k big_file.dat

# Decompress file in-place
bzip2 -d big_file.dat.bz2

```

| Flag | Description |
|------|-------------|
| `-d` | Decompress |
| `-k` | Keep original |
| `-v` | Verbose output |
| `-1 | -9` | Compression level (1=fast, 9=best) |

---

## Screenshots

<!-- ![description](../../assets/screenshots/linux/example.png) -->

---

## Notes / Gotchas

