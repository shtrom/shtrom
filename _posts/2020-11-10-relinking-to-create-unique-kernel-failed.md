---
id: 517
title: 'Relinking to create unique kernel&#8230; failed!'
date: '2020-11-10T22:13:29+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=517'
permalink: /2020/11/10/relinking-to-create-unique-kernel-failed/
iawp_total_views:
    - '10'
categories:
    - fix
    - oneliner
    - sysadmin
    - tip
tags:
    - OpenBSD
---

When using `syspatch` on OpenBSD, the upgrade sometimes fails with

```
Relinking to create unique kernel... failed!
!!! "/usr/libexec/reorder_kernel" must be run manually to install the new kernel
```

This generally happens after a system upgrade, or an otherwise manual change of kernel. This fix is to update the kernel hash, before re-running `reorder_kernel`.

```
# sha256 /bsd > /var/db/kernel.SHA256
# /usr/libexec/reorder_kernel 
```