---
id: 253
title: 'Exporting the SSL root store from Mac OS X&#8217;s Keychain'
date: '2016-06-20T10:50:48+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=253'
permalink: /2016/06/20/exporting-the-ssl-root-store-from-mac-os-xs-keychain/
categories:
    - code
    - oneliner
    - security
    - tip
tags:
    - Keychain
    - 'Mac OS X'
    - OpenSSL
    - Unix
---

```
security export -k /System/Library/Keychains/SystemRootCertificates.keychain -t certs -p
```

Useful for plain Unix/OpenSSL tools.