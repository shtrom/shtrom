---
id: 676
title: 'Relinking to create unique kernel&#8230; failed!'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=676'
permalink: '/?p=676'
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