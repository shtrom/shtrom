---
id: 586
title: 'Disabling DST Root CA X3'
date: '2022-10-28T13:21:33+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=586'
permalink: '/?p=586'
categories:
    - security
---

\* Let’s Encrypt https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/  
\* QNap QTS 4.3.3:  
\*\* openssl s\_client -showcerts -connect nassie.narf.ssji.net:453 | csplit – /END/1 {\*} ; openssl x509 -text -in xx00 | grep Not  
\*\* https://www.qnapclub.eu/fr/qpkg/238

\*\* not for QTS 4.3.3 / ARM), needs hacking: https://gist.github.com/shtrom/abc8ad8766af1287269900af12209095

\*\* now, this should work: curl https://acme-v02.api.letsencrypt.org/directory  
\* Debian: vim /etc/ca-certificates.conf; sudo update-ca-certificates  
\* Arch: sudo cp /etc/ca-certificates/extracted/cadir/DST\_Root\_CA\_X3.pem /etc/ca-certificates/trust-source/blacklist ; sudo update-ca-trust

<div class="wp-block-file">[CACert\_1.04\_QTS-4.3.3-ARM.tar.gz](https://blog.narf.ssji.net/7c623727-70f0-4583-80b8-7b584d5c7437)[Download](https://blog.narf.ssji.net/7c623727-70f0-4583-80b8-7b584d5c7437)</div>