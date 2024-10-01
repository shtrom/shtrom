---
id: 21
title: 'Booting OpenBSD installation from PXELINUX'
date: '2013-06-11T00:00:00+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://narf.jencuthbert.com/2013/06/11/pxelinux_openbsd_install/'
permalink: /2013/06/11/pxelinux_openbsd_install/
iawp_total_views:
    - '13'
categories:
    - sysadmin
tags:
    - chainloading
    - freedos
    - OpenBSD
    - PXE
    - pxeboot
    - pxechain.com
    - pxelinux
---

PXE-booting [OpenBSD](http://www.openbsd.org) is [easy and well documented](http://www.openbsd.org/cgi-bin/man.cgi?query=pxeboot&sektion=8&arch=i386). Unfortunately, it is not the case when more than just one OpenBSD install has to be made available through PXE. Using [PXELINUX](http://www.syslinux.org/wiki/index.php/PXELINUX) for multiplexing purposes has potential but the documentation is scarce, [unsuccessful](http://linux.derkeiler.com/Mailing-Lists/Debian/2008-01/msg02329.html), or [require patching the PXE loader](http://www.thegibson.org/blog/archives/10).

One trick which works is to [boot from a floppy disk image](http://www.smop.co.uk/mediawiki/index.php/PXE_booting_floppy_images), using [memdisk](http://www.syslinux.org/wiki/index.php/MEMDISK).

Adding the following to one’s <tt>pxelinux.cfg/default</tt> would do the trick just fine, and allow to start installing OpenBSD everywhere in a pinch!

```
LABEL openbsd53.i386
  MENU LABEL Open^BSD 5.3 i386
  KERNEL memdisk
  APPEND initrd=openbsd/5.3/i386/floppy53.fs
```

It’s probably not the nicest way to do it, but it is quick to get going, and works well.

*Update:* Or not… The <tt>floppy53.fs</tt> image boots fine, but is limited, starting with no DHCP support.

A bit more research revealed that [recent-ish versions (&gt;3.72) have a PXE boot chainloader](http://reboot.pro/topic/8088-multiple-pxelinux0-in-one-px-envoirement/?p=68789), found as <tt>modules/pxechain.com</tt> in the source. It can simply be use to chainload OpenBSD’s [pxeboot(8)](http://www.openbsd.org/cgi-bin/man.cgi?query=pxeboot&sektion=8&arch=amd64).

```
LABEL openbsd53.i386
  MENU LABEL Open^BSD 5.3 i386
  KERNEL pxechain.com
  APPEND ::/openbsd/5.3/i386/pxeboot
```

To smooth the process further, a <tt>/etc/[boot.conf(8)](http://www.openbsd.org/cgi-bin/man.cgi?query=boot.conf&sektion=8&arch=amd64)</tt>, can be created (within the TFTP root), to instruct [pxeboot(8)](http://www.openbsd.org/cgi-bin/man.cgi?query=pxeboot&sektion=8&arch=amd64) which kernel to boot. Unfortunately, the file doesn’t seem to be searched for within the path of [pxeboot(8)](http://www.openbsd.org/cgi-bin/man.cgi?query=pxeboot&sektion=8&arch=amd64), but from the root of the TFTP, which preclude the possibility of, *e.g.*, supporting multiple architectures.

```
boot openbsd/5.3/amd64/bsd.rd
```

Now it works!

*Update:* memdisk works well to boot [FreeDOS](http://www.freedos.org)!

```
LABEL freedos
MENU LABEL FreeDOS
KERNEL memdisk
APPEND initrd=/fdboot.img
```

*See also:* [More details on setting up PXE with DNSMASQ](https://blog.narf.ssji.net/2017/08/mitel-5212-sip-client-fritzbox-7390/).