---
id: 955
title: 'Parsing a CRL With OpenSSL'
date: '2023-08-04T09:23:22+10:00'
author: 'Olivier Mehani'
excerpt: 'https://langui.sh/2010/01/10/parsing-a-crl-with-openssl/'
layout: post
guid: 'https://blog.narf.ssji.net/?p=955'
permalink: /2023/08/04/parsing-a-crl-with-openssl/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
categories:
    - code
    - sysadmin
    - tip
tags:
    - OpenSSL
---

Just a shameless copy of [this post](https://langui.sh/2010/01/10/parsing-a-crl-with-openssl/) for my own records. Thanks Paul!

```
openssl crl -inform PEM -text -noout -in mycrl.crl
```

As to the `-inform`, `PEM` is for text data, or `DER` for binary data.