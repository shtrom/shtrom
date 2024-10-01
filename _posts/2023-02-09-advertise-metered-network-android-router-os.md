---
id: 773
title: 'Advertise a metered network to Android devices with Router OS'
date: '2023-02-09T23:40:53+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=773'
permalink: /2023/02/09/advertise-metered-network-android-router-os/
iawp_total_views:
    - '32'
image: /wp-content/uploads/sites/3/2023/02/image.png
categories:
    - sysadmin
    - tip
tags:
    - Android
    - Mikrotik
    - 'Router OS'
---

Due to an unplanned outage of my main ISP, I had to get a mobile data SIM in a hurry, to use as an [LTE backup uplink for my Mikrotik](https://blog.ligos.net/2018-03-01/Mikrotik-And-LTE-via-USB-and-Failover.html) hAP ac<sup>3</sup> (the whole setup of which I’ll describe one day). Given the price discrepancy of those, I wanted to make every transferred byte count: No unnecessary update fetching or immediate download of high-res sepia-toned photos of bulldogs in tutus.

[Android can advertise itself as a metered network to its (Android) clients](<http://* https://android.stackexchange.com/questions/215006/is-it-possible-to-designate-a-wi-fi-ssid-as-metered-mobile-network#220981>), so how do I do the same with Router OS 7?

**[(router agnostic) tl;dr](https://www.lorier.net/docs/android-metered.html):**

1. Make [DHCP Option 43 (Vendor-Specific Option)](https://www.rfc-editor.org/rfc/rfc2132#section-8.4) contain the string `ANDROID_METERED`;
2. The option should be sent even if not requested by the client (not standard compliant, but doesn’t hurt).

To set this up with Router OS, we need to manipulate three types of objects: DHCP options, DHCP options sets, and either DHCP servers or DHCP network ranges.

First, we [define the DHCP option itself](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPOptions.1).

<div class="wp-block-image"><figure class="aligncenter size-full">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/02/image.png)</figure></div>```
/ip/dhcp-server/option/add name=metered code=43 value="'ANDROID_METERED'"  force=yes
```

Two things to note here:

1. As of ROS 7.6, the `force` option is not available in WebFig, so it needs to be defined on the CLI either when `add`ing the option, or later with `set`. \[Update: as of ROS 7.7, the option is available in WebFig\]
2. For the `value` to be recognised as a string and encoded properly, it needs to be given with enclosing single quotes, then wrapped in double quotes (otherwise, a cryptic `failure: Unknown data type!` error will be given). See [*Properties* in the doc](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPOptions.1).

Once defined, the option needs to be added to a set. While no set is defined by default, it seems that as soon as a set exists, WebFig picks it up next time any server or network is edited. I opted to create a nondescript `default` set, with the idea that I can add/remove the `metered` option as needed, and have this reflected for all networks using the set.

```
/ip/dhcp-server/option/sets/add name=default options=metered
```

All that is left is to attach the set to the desired network(s) or server(s). As I was feeling zealous, I did both, but either one of them should be sufficient.

```
/ip/dhcp-server/set dhcp-option-set=default [find where name="dhcp"]
/ip/dhcp-server/network/set dhcp-option-set=default [find where address=192.168.88.0/24]
```

And this worked nicely! On the next DHCP response, the `Vendor-Option` was present with the right data.

```
23:54:20.862628 IP (tos 0x0, ttl 16, id 0, offset 0, flags [none], proto UDP (17), length 347)
    _gateway.bootps > laptop.example.net.bootpc: [udp sum ok] BOOTP/DHCP, Reply, length 319, xid 0x00000000, Flags [none] (0x0000)
	  Your-IP laptop.example.net
	  Server-IP server.example.net
	  Client-Ethernet-Address XX:XX:XX:XX:XX:XX (oui Unknown)
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x00000000
	    DHCP-Message (53), length 1: ACK
	    Subnet-Mask (1), length 4: 255.255.255.0
	    Default-Gateway (3), length 4: _gateway
	    Domain-Name-Server (6), length 8: _gateway,192.168.88.211
	    Domain-Name (15), length 16: "example.net"
	    NTP (42), length 4: _gateway
	    <strong>Vendor-Option (43), length 15: 65.78.68.82.79.73.68.95.77.69.84.69.82.69.68</strong>
	    Lease-Time (51), length 4: 86399
	    Server-ID (54), length 4: _gateway
	    END (255), length 0
```

This in turn was sufficient for Android devices to consider the network as metered. Job done!

<figure class="wp-block-image size-full">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/02/signal-2023-02-08-002135.png)</figure>