# Windows CLI

## Find a File

Search Windows directory recursively for notepad.exe:
```cmd
where /R C:\Windows notepad.exe

C:\Windows\notepad.exe
C:\Windows\System32\notepad.exe
C:\Windows\SysWOW64\notepad.exe
```
- `/R` - recursively searches the specified directory and all subdirectories

Search entire C: drive for files containing "password":

```cmd
dir /a /s /b C:\*password*.txt

C:\Program Files\Common Files\System\en-US\super secret system passwords.txt
C:\Users\Administrator\super secret admin passwords.txt
C:\Users\User03\Desktop\super secret user03 passwords.txt
```
- `/a` - include hidden and system files in the search
- `/s` - search subdirectories recursively
- `/b` - bare format - paths only, no headers or summary lines
- Can also pipe (|) to `findstr`, but i've had mixed results with find/findstr

---

## Read a File

Dump entire file contents at once:
```cmd
type "C:\Users\Administrator\super secret admin passwords.txt"

password
1234567
rockyou
12345678
abc123
6987
69866986
```

Page through file contents one screen at a time:
```cmd
more "C:\Users\Administrator\super secret admin passwords.txt"

password
1234567
rockyou
12345678
abc123
6987
69866986
```

---

## Create a File

Create a new file with text content:
```cmd
echo test content > C:\Users\User03\Desktop\test.txt

more C:\Users\User03\Desktop\test.txt
test content
```

Append command output to a file:
```cmd
netstat -a >> "C:\Users\User03\Desktop\network connections.txt"

Active Connections

  Proto  Local Address          Foreign Address        State
  TCP    0.0.0.0:135            DESKTOP-R4EM499:0      LISTENING
  TCP    0.0.0.0:445            DESKTOP-R4EM499:0      LISTENING
  TCP    192.168.8.201:49271    20.59.87.225:https     ESTABLISHED
  ...
```
- `>` - creates/overwrites the file
- `>>` - appends to an existing file

---

## Change File Permissions (icacls)

View current permissions on a folder:
```cmd
icacls C:\Users\Public\Documents

C:\Users\Public\Documents BUILTIN\Administrators:(I)(OI)(CI)(F)
                          NT AUTHORITY\SYSTEM:(I)(F)
                          CREATOR OWNER:(I)(OI)(CI)(IO)(F)
                          NT AUTHORITY\INTERACTIVE:(I)(OI)(CI)(M,DC)
Successfully processed 1 files; Failed processing 0 files
```

Deny full control to a specific user:
```cmd
icacls C:\Users\Public\Documents /deny User03:(OI)(CI)(F)

processed file: C:\Users\Public\Documents
Successfully processed 1 files; Failed processing 0 files
```

Attempt to grant access back:
```cmd
icacls C:\Users\Public\Documents /grant User03:(OI)(CI)(F)

C:\Users\Public\Documents: Access is denied.
Successfully processed 0 files; Failed processing 1 files
```

**Permission flags:**
| Flag | Description |
|---|---|
| `(OI)` | Object Inherit; applies to files within the folder |
| `(CI)` | Container Inherit; applies to subfolders |
| `(F)` | Full control |
| `(M)` | Modify |
| `(R)` | Read |
| `(W)` | Write |

![icacls1](../../assets/screenshots/windows/icacls1.png)

## Recovering denied permissions

Use `takeown` to reclaim ownership before removing the deny entry:
```cmd
takeown /F C:\Users\Public\Documents /R /A

SUCCESS: The file (or folder): "C:\Users\Public\Documents" now owned by the administrators group.
Do you want to replace the directory permissions with permissions granting you
full control ("Y" for YES, "N" for NO or "C" to CANCEL)? y
SUCCESS: The file (or folder): "C:\Users\Public\Documents\desktop.ini" now owned by the administrators group.
...
```

Remove the specific deny entry for the user:
```cmd
icacls C:\Users\Public\Documents /remove:d User03

processed file: C:\Users\Public\Documents
Successfully processed 1 files; Failed processing 0 files
```

Verify the deny entry is gone:
```cmd
icacls C:\Users\Public\Documents

C:\Users\Public\Documents BUILTIN\Administrators:(OI)(IO)(F)
                          BUILTIN\Administrators:(CI)(F)
                          BUILTIN\Administrators:(I)(OI)(CI)(F)
                          CREATOR OWNER:(I)(OI)(CI)(IO)(F)
                          NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
Successfully processed 1 files; Failed processing 0 files
```

**Flags:**
| Flag | Description |
|---|---|
| `/F` | Specifies the file or folder |
| `/R` | Recursive - applies to all subfolders and files |
| `/A` | Gives ownership to the Administrators group instead of current user |
| `/remove:d` | Removes only deny entries for the specified user |

![icacls2](../../assets/screenshots/windows/icacls2.png)

---

## List Users

List all local user accounts:
```cmd
net user

User accounts for \\DESKTOP-R4EM499

-------------------------------------------------------------------------------
Administrator            DefaultAccount           Guest
User03                   WDAGUtilityAccount
The command completed successfully.
```

Attempt domain query on a standalone machine:
```cmd
net user /domain

The request will be processed at a domain controller for domain WORKGROUP.
System error 1355 has occurred.
The specified domain either does not exist or could not be contacted.
```

---

## Create a User

Create a new local user with a password:
```cmd
net user testuser P@ssw0rd123! /add

The command completed successfully.
```

Verify:
```cmd
net user

User accounts for \\DESKTOP-R4EM499

-------------------------------------------------------------------------------
Administrator            DefaultAccount           Guest
testuser                 User03                   WDAGUtilityAccount
The command completed successfully.
```

Delete the user:
```cmd
net user testuser /delete

The command completed successfully.
```

---

## List Groups

List all local groups:
```cmd
net localgroup

Aliases for \\DESKTOP-R4EM499

-------------------------------------------------------------------------------
*Administrators
*Device Owners
*Distributed COM Users
*Event Log Readers
*Guests
*Hyper-V Administrators
*IIS_IUSRS
*OpenSSH Users
*Performance Log Users
*Performance Monitor Users
*Remote Management Users
*System Managed Accounts Group
*User Mode Hardware Operators
*Users
The command completed successfully.
```

---

## Create a Group

Create the new local group:
```cmd
net localgroup SuperSoldiers /add

The command completed successfully.
```

Add member to group:
```cmd
net localgroup SuperSoldiers /add User03
```

Verify:
```cmd
net localgroup SuperSoldiers

Alias name     SuperSoldiers
Comment

Members

-------------------------------------------------------------------------------
User03
The command completed successfully.
```

Delete the group:
```cmd
net localgroup SuperSoldiers /delete

The command completed successfully.
```

---

## List Shares

List all active shares:
```cmd
net share

Share name   Resource                        Remark

-------------------------------------------------------------------------------
C$           C:\                             Default share
IPC$                                         Remote IPC
ADMIN$       C:\WINDOWS                      Remote Admin
The command completed successfully.
```

---

## Create a Share

Create a new share, grant Everyone read-only access
```cmd
net share Media_Share=C:\SharedMedia /GRANT:Everyone,READ
```
- `/GRANT:Everyone,READ` - grants Everyone read-only access to the share

Verify share was added with `net share` again

```cmd
net share

Share name   Resource                        Remark

-------------------------------------------------------------------------------
C$           C:\                             Default share
IPC$                                         Remote IPC
ADMIN$       C:\WINDOWS                      Remote Admin
Media_Share  C:\SharedMedia
The command completed successfully.
```

![shared folder verify](../../assets/screenshots/windows/shared1.png)
![shared folder permissions](../../assets/screenshots/windows/shared2.png)

---

## Notes / Gotchas
- `net user /domain` and `net localgroup /domain` fail with "System error 1355" on a standalone machine
  - These commands require an actual domain controller
- `net group` (without `localgroup`) only works with a Domain Controller
  - Use `net localgroup` on standalone machines
- Once `icacls /deny` is applied, even `/grant` afterward can fail with "Access is denied" because deny rules take precedence over grant rules in NTFS
  - Use `takeown` to take back ownership, then `icacls /remove:d` to clear the deny entry
