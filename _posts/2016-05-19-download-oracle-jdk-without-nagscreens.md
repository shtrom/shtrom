---
id: 248
title: 'Download Oracle JDK without nagscreens'
date: '2016-05-19T18:51:25+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=248'
permalink: /2016/05/19/download-oracle-jdk-without-nagscreens/
categories:
    - idiotic
    - oneliner
    - tip
tags:
    - JDK
    - Jenkins
    - Oracle
---

With `M` as the major, `m` as the minor, and `r` as the revision,

```
export M=8 m=65 r=17; wget --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/${M}u${m}-b${r}/jdk-${M}u${m}-linux-x64.tar.gz
```

Useful for scripting, headless operation, continuous integration, and just for any time when one doesn’t have any for unneeded account creation.