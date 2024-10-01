---
id: 802
title: 'PXE-booting ArchLinux Install ISO'
date: '2023-02-09T23:48:45+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=802'
permalink: '/?p=802'
---

https://wiki.archlinux.org/index.php/PXE#Server\_setup

fstab

 /data/software/Linux/archlinux-2015.02.01-dual.iso /run/archiso/bootmnt iso9660 auto,noexec 0 0

exportfs

 /run/archiso/bootmnt/ 192.168.103.0/24(ro,async,subtree\_check,no\_root\_squash)

exportfs -v

 lrwxrwxrwx 1 root root 21 Feb 16 21:34 archiso -&gt; /run/archiso/bootmnt/  
 lrwxrwxrwx 1 root root 17 Feb 16 21:44 boot -&gt; archiso/arch/boot  
 lrwxrwxrwx 1 root root 38 Feb 16 21:36 ldlinux.c32 -&gt; archiso/arch/boot/syslinux/ldlinux.c32  
 lrwxrwxrwx 1 root root 39 Feb 16 21:41 libcom32.c32 -&gt; archiso/arch/boot/syslinux/libcom32.c32  
 lrwxrwxrwx 1 root root 38 Feb 16 21:41 libutil.c32 -&gt; archiso/arch/boot/syslinux/libutil.c32  
 lrwxrwxrwx 1 root root 38 Feb 16 21:35 pxelinux.0 -&gt; archiso/arch/boot/syslinux/lpxelinux.0

 LABEL archnetinst  
 MENU LABEL ^ArchLinux Network Install  
 CONFIG archiso/arch/boot/syslinux/archiso\_pxe\_choose.cfg