---
id: 563
title: 'New router'
date: '2022-10-28T13:21:33+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=563'
permalink: '/?p=563'
categories:
    - hardware
    - Uncategorised
tags:
    - Mikrotik
    - 'Router OS'
    - wip
---

\* Comparison fritz/peplink/otherone/mikrotik routersecurity https://routersecurity.org/SecureRouters.php https://www.routersecurity.org/bugs.php  
\*\* ipv6 issue https://forum.peplink.com/t/ipv6-support/3675/36  
\*\* still dodgy on mikrotik https://forum.mikrotik.com/viewtopic.php?p=872986&amp;sid=408d9366682782dc2d21c1e190dc72bc  
\* vlans https://forum.mikrotik.com/viewtopic.php?f=13&amp;p=875086&amp;t=177865&amp;sid=8756b5ba5b3e5b31506581b9f59afedb  
\* mikrotik  
\* vlan https://forum.mikrotik.com/viewtopic.php?p=781603  
\* dhcp-pd /64 for subnetting /56  
\* dhcp  
\*\* ntp https://mikrotik.com/download npk installed on reboot

\*\*\* ntp pool https://wiki.mikrotik.com/wiki/Manual:Scripting-examples#Allow\_use\_of\_ntp.org\_pool\_service\_for\_NTP

\*\*\* https://forum.mikrotik.com/viewtopic.php?p=890894#p890894  
\*\* tftp started on reboot  
\*\* ddns updates + 2 links (dhcp + periodic script) confirm permissions  
\*\*\* https://blog.pessoft.com/2019/09/06/mikrotik-script-automatic-dns-records-from-dhcp-leases/  
\*\*\* https://www.ctrl.blog/entry/routeros-dhcp-lease-script.html