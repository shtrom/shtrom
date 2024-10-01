---
id: 960
title: 'Parsing a CRL With OpenSSL'
date: '2023-08-04T09:26:35+10:00'
author: 'Olivier Mehani'
excerpt: 'https://langui.sh/2010/01/10/parsing-a-crl-with-openssl/'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=960'
permalink: '/?p=960'
---

Just a shameless copy of [this post](https://langui.sh/2010/01/10/parsing-a-crl-with-openssl/) for my own records. Thanks Paul!

```
openssl crl -inform PEM -text -noout -in mycrl.crl
```

As to the `-inform`, `PEM` is for text data, or `DER` for binary data.