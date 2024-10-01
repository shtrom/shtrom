---
id: 793
title: 'Download Oracle JDK without nagscreens'
date: '2023-02-09T23:48:44+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=793'
permalink: '/?p=793'
---

With `M` as the major, `m` as the minor, and `r` as the revision,

```
export M=8 m=65 r=17; wget --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/${M}u${m}-b${r}/jdk-${M}u${m}-linux-x64.tar.gz
```

Useful for scripting, headless operation, continuous integration, and just for any time when one doesn’t have any for unneeded account creation.