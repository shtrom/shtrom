---
id: 794
title: 'Let&#8217;s Encrypt on OpenBSD'
date: '2023-02-09T23:48:44+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=794'
permalink: '/?p=794'
---

```
$ sudo pkg_add augeas
```

No Dialog tool (what is it?), so text mode

```
$ ./letsencrypt-auto certonly -t --webroot \
  -w /srv/www/sites/narf.ssji.net/www -d www.narf.ssji.net -d ns1.narf.ssji.net \
  -w /srv/www/sites/narf.ssji.net/scm -d scm.narf.ssji.net \
  -w /srv/www/sites/mehani.name/www  -d mehani.name -d www.mehani.name \
  -w /srv/www/sites/mehani.name/olivier -d olivier.mehani.name \
  -w /srv/www/sites/mehani.name/roland -d roland.mehani.name \
  #-w /srv/www/sites/mehani.name/martine -d martine.mehani.name \
  #-w /srv/www/sites/mehani.name/thomas -d thomas.mehani.name \
  -w /srv/www/sites/rantmyhouse.info/www -d rantmyhouse.info -d www.rantmyhouse.info \
  -w /srv/www/wordpress -d blog.narf.ssji.net -d blog.rantmyhouse.info \
   -d consumeristadventures.info -d www.consumeristadventures.info \
   -d neilcuthbert.co.uk -d www.neilcuthbert.co.uk \
 -w /srv/www/wallabag -d wallabag.narf.ssji.net \
 -w /srv/www/owncloud -d cloud.narf.ssji.net  \
 -w /srv/www/roundcubemail -d mail.narf.ssji.net
```

Webroot: allow direct access to `.well-known/acme-challenge` (ownCloud, Redmine, …). See https://community.letsencrypt.org/t/issue-creating-certificate-for-owncloud/7280.

```
RewriteRule ^\.well-known/acme-challenge - [L]
```

httpd conf

```
SSLCertificateFile    /etc/letsencrypt/live/www.narf.ssji.net/cert.pem
SSLCertificateChainFile /etc/letsencrypt/live/www.narf.ssji.net/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/www.narf.ssji.net/privkey.pem
```

Restart

```
$ sudo rcctl restart apache
apache(ok)
apache(ok)
```

```
$ openssl s_client -connect localhost:443 | grep issuer=
 depth=0 CN = www.narf.ssji.net
 verify error:num=20:unable to get local issuer certificate
 verify return:1
 depth=0 CN = www.narf.ssji.net
 verify error:num=27:certificate not trusted
 verify return:1
 depth=0 CN = www.narf.ssji.net
 verify error:num=21:unable to verify the first certificate
 verify return:1
 issuer=/C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X1
```

Adding the SSLCertificateChainFile

```
$ openssl s_client -connect localhost:443 | grep issuer=
depth=1 C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X1
verify error:num=20:unable to get local issuer certificate
verify return:0
issuer=/C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X1
DONE
```

doesn’t work:

```
$ (echo; echo letsencrypt; curl https://letsencrypt.org/certs/isrgrootx1.pem https://letsencrypt.org/certs/lets-encrypt-x1-cross-signed.pem https://letsencrypt.org/certs/letsencryptauthorityx1.pem https://letsencrypt.org/certs/lets-encrypt-x2-cross-signed.pem https://letsencrypt.org/certs/letsencryptauthorityx2.pem | sed s/^M//) | sudo tee -a /etc/ssl/cacert.pem
```

## Nginx and webapps

```
        # Redirect Let's Encrypt challenges to a static location
        location /.well-known/acme-challenge/ {
                alias /srv/www/.well-known/acme-challenge/;
        } 
```

```
        ssl_stapling on;
        #ssl_trusted_certificate /etc/ssl/cacert-bundle.crt;
        ssl_certificate /etc/letsencrypt/live/supahwinch.narf.ssji.net/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/supahwinch.narf.ssji.net/privkey.pem;
```

## ldapd

php-ldap issues

```
TLS: peer cert untrusted or revoked (0x42)
TLS: can't connect: (unknown error code).
```

ldapd.conf

```
listen on sis0 ldaps certificate "letsencrypt"
```

Getting the certificates (need http or standalone)

```
$ ./letsencrypt-auto certonly -t --webroot \
    -w /srv/www/sites/narf.ssji.net/www -d ldap.narf.ssji.net \
                                        -d ldap1.narf.ssji.net
$ sudo ln -sf ../../letsencrypt/live/www.narf.ssji.net/fullchain.pem /etc/ldap/certs/letsencrypt.crt
$ sudo ln -sf ../../letsencrypt/live/www.narf.ssji.net/privkey.pem /etc/ldap/certs/letsencrypt.key
```

END