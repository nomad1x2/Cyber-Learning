# View Windows Logs

## Overview

Windows Event Viewer (`eventvwr.msc`) is gui based and records system, security, and application events into separate logs
- Each log category covers a different scope

Can also use powershell to get logs

---

## Log Categories

| Log  | Description |
|----|----|
| Application  | The Application log contains events logged by applications or programs. For example, a database program might record a file error in the application log. Program developers decide which events to log |
| Security  | Contains events such as valid and invalid logon attempts, as well as events related to resource use such as creating, opening, or deleting files or other objects. An administrator can start auditing to record events in the security log |
| Setup   | The Setup log contains events related to application setup |
| System  | Contains events logged by system components, such as the failure of a driver or other system component to load during startup |
| ForwardedEvents  | The ForwardedEvents log is used to store events collected from remote computers. To collect events from remote computers, you must create an event subscription |

Ref:
- https://learn.microsoft.com/en-us/windows/win32/eventlog/eventlog-key
- https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc722404(v=ws.10)

---

## Viewing Logs via Event Viewer (GUI)

1. Open `eventvwr.msc`
2. Expand **Windows Logs**
3. Select a category to view, double click any event for full details

![event viewer windows logs](../../assets/images/windows/eventviewer1.png)

---

## Viewing Logs via PowerShell

```powershell
Get-EventLog -LogName Application -Newest 5

Index Time          EntryType   Source                 InstanceID Message
----- ----          ---------   ------                 ---------- -------
1789  Jun 21 01:55  Information Software Protecti...   1073758208 Successfully scheduled Software Protection serv...
1788  Jun 21 01:54  Information Software Protecti...   3221241866 Offline downlevel migration succeeded.
```

```powershell
Get-EventLog -LogName System -Newest 5

Index Time          EntryType   Source                 InstanceID Message
----- ----          ---------   ------                 ---------- -------
3244  Jun 21 01:59  Information Display                      4107 A caller specified the SDC_FORCE_MODE_ENUMERATI...
3242  Jun 21 01:49  Warning     Microsoft-Windows...           47 Time Provider NtpClient: No valid response has ...
```

```powershell
Get-EventLog -LogName Security -Newest 5

Index Time          EntryType    Source                 InstanceID Message
----- ----          ---------    ------                 ---------- -------
44735 Jun 21 02:00  SuccessA...  Microsoft-Windows...         5379 Credential Manager credentials were read....
```

View full detail on a single event:
```powershell
Get-EventLog -LogName Security -Newest 1 | format-list *

EventID            : 5379
MachineName        : DESKTOP-R4EM499
EntryType          : SuccessAudit
Message            : Credential Manager credentials were read.
                     Subject:
                        Security ID:            S-1-5-21-3939449205-2192989374-528527534-1001
                        Account Name:           User03
                        Logon ID:               0x3524a
                        Read Operation:         %%8100
Source             : Microsoft-Windows-Security-Auditing
TimeGenerated      : 6/21/2026 2:00:01 AM
....
```

---

## Entry Types

| Type | Meaning |
|----|----|
| Information | Indicates that a change in an application or component has occurred, such as an operation has successfully completed, a resource has been created, or a service started |
| Warning | Indicates that an issue has occurred that can impact service or result in a more serious problem if action is not taken |
| Error | Indicates that a problem has occurred, which might impact functionality that is external to the application or component that triggered the event |
| Critical | Indicates that a failure has occurred from which the application or component that triggered the event cannot automatically recover |
| SuccessAudit | An audited action succeeded (logons, credential reads, object access) |
| FailureAudit | An audited action failed (failed logon attempts, denied access) |

Ref:
- https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/cc765981(v=ws.10)

---

## Notes / Gotchas
- `Get-EventLog` is older and migrating to the `Get-WinEvent` cmdlet, which supports newer log formats and better filtering, but `Get-EventLog` still works on Windows 11
- Security log requires audit policy to be configured to capture meaningful events, by default many audit categories are disabled
- `format-list *` on a single event shows every property, but in powershell you can select individual properties also