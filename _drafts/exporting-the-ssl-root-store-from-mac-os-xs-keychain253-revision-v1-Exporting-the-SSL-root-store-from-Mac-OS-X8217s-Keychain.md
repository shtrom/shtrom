---
id: 792
title: 'Exporting the SSL root store from Mac OS X&#8217;s Keychain'
date: '2023-02-09T23:48:44+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=792'
permalink: '/?p=792'
---

```
security export -k /System/Library/Keychains/SystemRootCertificates.keychain -t certs -p
```

Useful for plain Unix/OpenSSL tools.