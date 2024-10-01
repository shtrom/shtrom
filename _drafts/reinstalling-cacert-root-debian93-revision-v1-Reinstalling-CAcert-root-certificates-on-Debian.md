---
id: 804
title: 'Reinstalling CAcert root certificates on Debian'
date: '2023-02-09T23:48:45+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=804'
permalink: '/?p=804'
---

[CAcert](http://www.cacert.org/) is an SSL Certificate Authority based on the establishment of a web-of-trust à la PGP: rather than charging to issue certificates to anyone, it issues them only to members who have been vouched for by enough other trustworthy members (assurers).

For historical reasons, they were included in the [Debian ca-certificates package](https://packages.debian.org/search?keywords=ca-certificates). It was however [recently removed](http://www.debian.org/News/weekly/2014/07/#CAcert), for [justified reasons](https://lwn.net/Articles/590879/) (CAcert is conducting an audit, and withdrew their demand for inclusion in the Mozilla chain until it’s done). Most other distributions mirror from this package to ship their root certificate, and have also dropped CAcert as a consequence.

This is however a bit annoying, as many sites started popping up warnings due to their root certificate not being in the trusted chain of the OS anymore. Until, maybe, they are [reinstalled but disabled by default](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=718434#87), I quickly wrote up [a tiny script that downloads CAcert’s root certificates, and re-registers them](https://scm.narf.ssji.net/svn/shtrom/browser/scripts/reinstall-cacert.org_certs.sh). It’s quick and dirty, and only does an MD5 sum to make check they are the right ones, so use at your own risks.

For reference, the MD5 are as follows:

```
MD5_ROOT=fb262d55709427e2e9acadf2c1298c99 # http://www.cacert.org/certs/root.crt
MD5_CLASS3=95c1c1820c0ed1de88d512cb10e25182 # http://www.cacert.org/certs/class3.crt
```

Also, note that the script installs the certs as a single concatenated file, while I seem to understand that Debian switched to installing them separately for some reason. I am not sure what difference it makes.