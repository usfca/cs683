 
=

Penetration testing
===================

What you will need:
-------------------

-   Metaspoit (Kali linux or local download)

-   Metaspoitable 2
    https://metasploit.help.rapid7.com/docs/metasploitable-2-exploitability-guide

What metasploit
---------------

A penetration testing tool, contains a database of exploits that can be run in a
number of different environments and attack a number of different machines. Each
attack has a description and a target which can range from a specific version of
an operating system to certain software vunerablitlies.

| Package         | Description                                                                                                                                                                                  |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Exploit         | Can take advantage of a vulnerable machine and can attach a payload onto the target machine.                                                                                                 |
| Auxiliary       | Will give you attacks that allow you to perform reconnaissance on a victims machines and perform other types of attacks such as DDOS                                                         |
| Payloads        | Files that are left on the target system that allows the attack to control the target system                                                                                                 |
| Encoders        | Used to re-encode payloads and exploit and is important for stealth and evasion                                                                                                              |
| Nops            | No operation: causes the systems to do nothing for an entire clock cycle ( Allow you to execute code on target machines)                                                                     |
| Post            | Contains scripts that allow you to continue to attack a exploited machine                                                                                                                    |
| Useful Commands | Description                                                                                                                                                                                  |
| Help command    | Provides a list of commands that you can use with metaspoit                                                                                                                                  |
| Use             | Loads a exploit onto memory so it can be used in an attack (use exploit/windows/browser/(some exploit)                                                                                       |
| Show            | This command will give you information about a specific exploit including the information for the exploit and what machines it can target                                                    |
| Show Options    | More specific information on what arguments this exploit takes                                                                                                                               |
| Set [option]    | this is used to set the options shown above                                                                                                                                                  |
| Show info       | Will give an explanation in plain english on how to exploit and what a specific exploit is used for                                                                                          |
| Search          | example search type:exploit platform:windows flash. First argument it takes is the type of module you are a looking for and the Second argument is to show which platform you want to attack |
| Exploit         | this is used to run an exploit that is loaded into the memory                                                                                                                                |

Metaspoitable 2
---------------

This is an operating system designed from the ground up to be vunerable to
attack. One of the things that this operating system allows you to do it that it
has several different preloaded websevers that can be used to practice anything
from penetration testing to web hacking. It also allows you to change the
security level to practice in different environments. Typically one would use a
Virtual environment to intialize the os but you could also use a PI or even
anouther machine.
