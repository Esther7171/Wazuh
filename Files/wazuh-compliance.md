
| **Setting**                                                                 | **Status**                                                              |
|-----------------------------------------------------------------------------|-------------------------------------------------------------------------|
| Length of password                                                           | 14>=24 char [English uppercase characters (A through Z) - English lowercase characters (a through z) - Base 10 digits (0 through 9) - Non-alphabetic characters (for example, !, $, #, %) o A catch-all category of any Unicode character] |
| Maximum password age                                                         | 60 days                                                                  |
| Minimum password age                                                         | 7 days                                                                   |
| Account lockout duration                                                     | 15 or more minutes                                                       |
| Account lockout threshold                                                    | 5 or fewer invalid logon attempt(s), but not 0                            |
| Reset account lockout counter after                                          | 15 or more minute(s)                                                     |
| Accounts: Administrator account status                                       | Disabled                                                                 |
| Accounts: Block Microsoft accounts                                           | Users can't add or log on with Microsoft accounts                        |
| Accounts: Guest account status                                               | Disabled                                                                 |
| Accounts: Limit local account use of blank passwords to console logon only   | Enabled                                                                  |
| Accounts: Rename administrator account                                       |                                                                         |
| Audit: Force audit policy subcategory settings                               | Enabled                                                                  |
| Audit: Shut down system immediately if unable to log security audits        | Disabled                                                                 |
| Devices: Allowed to format and eject removable media                         | Administrators and Interactive Users                                      |
| Devices: Prevent users from installing printer drivers                       | Enabled                                                                  |
| Domain member: Digitally encrypt or sign secure channel data                | Enabled                                                                  |
| Interactive logon: Don't display last signed-in                              | Enabled                                                                  |
| Interactive logon: Machine account lockout threshold                         | 10 or fewer invalid logon attempts, but not 0                             |
| Interactive logon: Machine inactivity limit                                  | 900 or fewer second(s), but not 0                                        |
| Interactive logon: Message text for users attempting to log on              |                                                                         |
| Interactive logon: Prompt user to change password before expiration          | between 5 and 14 days                                                    |
| Interactive logon: Smart card removal behavior                               | Lock Workstation or higher                                              |
| Microsoft network client: Digitally sign communications                      | Enabled                                                                  |
| Microsoft network client: Digitally sign communications (if server agrees)  | Enabled                                                                  |
| Microsoft network client: Send unencrypted password to third-party SMB servers | Disabled                                                             |
| Microsoft network server: Server SPN target name validation level           | Accept if provided by client                                              |
| Network access: Allow anonymous SID/Name translation                         | Disabled                                                                 |
| Network access: Do not allow anonymous enumeration of SAM accounts and shares | Enabled                                                             |
| Network access: Do not allow storage of passwords and credentials for network authentication | Enabled                               |
| Network access: Let Everyone permissions apply to anonymous users           | Disabled                                                                 |
| Network access: Named Pipes that can be accessed anonymously                | None                                                                     |
| Configure use of hardware-based encryption for removable data drives        | Enabled                                                                  |
| Configure use of hardware-based encryption for removable data drives: Use BitLocker software-based encryption when hardware encryption is not available | Enabled: True                        |
| Configure use of hardware-based encryption for removable data drives: Restrict encryption algorithms and cipher suites allowed for hardware-based encryption | Enabled: False                      |
| Configure use of hardware-based encryption for removable data drives: Restrict crypto algorithms or cipher suites to the following | Enabled: 2.16.840.1.101.3.4.1.2;2.16.840.1.101.3.4.1.42   |
| Configure use of passwords for removable data drives                        | Disabled                                                                 |
| Configure use of smart cards on removable data drives                       | Enabled                                                                  |
| Configure use of smart cards on removable data drives: Require use of smart cards on removable data drives | Enabled: True          |
| Deny write access to removable drives not protected by BitLocker            | Enabled                                                                  |
| Deny write access to removable drives not protected by BitLocker: Do not allow write access to devices configured in another organization | Enabled: False            |
| Choose drive encryption method and cipher strength (Windows 10 [Version 1511] and later) | Enabled: XTS-AES 256-bit                |
| Turn off Microsoft consumer experiences                                     | Enabled                                                                  |
| Do not display the password reveal button                                   | Enabled                                                                  |
| Enumerate administrator accounts on elevation                               | Disabled                                                                 |
| Allow Telemetry                                                              | Enabled: 0 - Security [Enterprise Only]                                   |
| Disable pre-release features or settings                                    | Disabled                                                                 |
| Do not show feedback notifications                                          | Enabled                                                                  |
| Toggle user control over Insider builds                                      | Disabled                                                                 |
| Download Mode                                                                | Enabled: None or LAN or Group or Disabled                                |
| EMET 5.5 or higher is installed                                              | Enabled                                                                  |
| Default Action and Mitigation Settings                                       | Enabled                                                                  |
| Default Protections for Internet Explorer                                   | Enabled                                                                  |
| Default Protections for Popular Software                                    | Enabled                                                                  |
| Default Protections for Recommended Software                                | Enabled                                                                  |
| System ASLR                                                                  | Enabled: Application Opt-In                                              |
| System DEP                                                                   | Enabled: Application Opt-Out                                             |
| System SEHOP                                                                 | Enabled: Application Opt-Out                                             |
| Application: Control Event Log behavior when the log file reaches its maximum size | Disabled                                                             |
| Application: Specify the maximum log file size (KB)                         | Enabled: 32,768 or greater                                               |
| Security: Control Event Log behavior when the log file reaches its maximum size | Disabled                                                             |
| Security: Specify the maximum log file size (KB)                            | Enabled: 196,608 or greater                                              |
| Setup: Control Event Log behavior when the log file reaches its maximum size | Disabled                                                             |
| Setup: Specify the maximum log file size (KB)                               | Enabled: 32,768 or greater                                               |
| System: Control Event Log behavior when the log file reaches its maximum size | Disabled                                                             |
| System: Specify the maximum log file size (KB)                              | Enabled: 32,768 or greater                                               |
| Configure Windows SmartScreen                                                | Enabled: Require approval from an administrator before running downloaded unknown software |
| Turn off Data Execution Prevention for Explorer                             | Disabled                                                                 |
| Turn off heap termination on corruption                                      | Disabled                                                                 |
| Turn off shell protocol protected mode                                      | Disabled                                                                 |
