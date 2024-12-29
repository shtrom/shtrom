---
id: 288
title: 'Using Let&#8217;s Encrypt certificates with a FRITZ!Box'
date: '2017-07-17T22:58:32+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=288'
permalink: /2017/07/17/using-lets-encrypt-certificates-with-a-fritzbox/
iawp_total_views:
    - '57'
image: /wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-17-22-49-24.png
categories:
    - security
    - sysadmin
    - tip
tags:
    - FRITZ!Box
    - FRITZ!OS
    - 'Let''s Encrypt'
    - SSL
    - TLS
---

Today, when trying to log in remotely to my home router (a [FRITZ!Box)](https://en.avm.de/products/fritzbox/), I was greeted with an TLS certificate error. I was pretty sure it’s my router, but am I really keen to type in a password into a field that I have no idea whether it is actual my machine, or a nice-looking replica? A clear indication that it is time to use a better cert than a self-signed one that I cannot verify remotely.

I use [Let’s Encrypt](https://letsencrypt.org/) for all my other certificates, so why not use it on my router? However, I found precious little information about how to use it with the FRITZ!Box. Fortunately, it’s pretty straightforward.

There is no obvious way to run `certbot` straight onto the router, except perhaps when running [Freetz](http://freetz.org/), but that is not my case (yet?). So I’m still running FRITZ!OS (6.83 at the time of this writing) which, though not entirely free and sometimes annoying, generally works well.

The next best choice is simply to use `certbot` on a machine behind the router, with adequate redirection of its port 80 from the box (it’s actually my public server, in the DMZ).

<figure class="wp-caption thumbnail aligncenter" id="attachment_291" style="width: 300px;">[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-17-22-33-40-300x221.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-17-22-33-40.png) <figcaption class="wp-caption-text">Forwarding port 80 from the FRITZ!Box to an internal server</figcaption></figure>

The next step is, simply, to run `cerbot` as usual on the internal server, with the desired domain. I prefer the webroot method, as it doesn’t require restarting my webserver.

```
sudo certbot certonly -d ${DOMAIN} --webroot --webroot-path /var/www/
```

Once the certificate issued, all the cryptographic material ends up in `/etc/letsencrypt`, in either `live` of `keys`, for the certificate and private key, respectively.

We need to [transfer both those files to the FRITZ!Box](https://en.avm.de/service/fritzbox/fritzbox-7360/knowledge-base/publication/show/1525_Importing-your-own-certificate-to-the-FRITZ-Box/), but the relevant form only allows one file to be uploaded, in PEM format. PEM has this nice property that, thanks to its delimiter, multiple files can be concatenated into one. This turns out to be just what the FRITZ!Box needs.

```
sudo cat /etc/letsencrypt/live/${DOMAIN}/privkey.pem /etc/letsencrypt/live/${DOMAIN}/fullchain.pem > ~/fritz.pem
```

<figure class="wp-caption thumbnail aligncenter" id="attachment_292" style="width: 300px;">[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-17-22-34-32-300x219.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-17-22-34-32.png) <figcaption class="wp-caption-text">Uploading a Let’s Encrypt key and certificate to the FRITZ!Box</figcaption></figure>

Note that this file is pretty sensitive, so one would do well do delete any other copy of it once uploaded to the router.

<figure class="wp-caption thumbnail aligncenter" id="attachment_293" style="width: 300px;">[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-17-22-49-24-300x281.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-17-22-49-24.png) <figcaption class="wp-caption-text">Done!</figcaption></figure>

A remaining issue is to automate the renewal of the certificate when needed. `certbot` will do it automatically if set up to do so (e.g., via cron or other scheduling mechanism), but the upload part still needs to be manual; the main issue is that FRITZ!OS is pretty-close to a one-page app now, and there doesn’t seem to be any canonical URL that can be used to upload the renewed certificate with, e.g., cURL.

**EDIT 2018-08-15**: As discussed in the comments below, there are ways to use the FRITZ!Box API endpoints to automatically upload the certificate. Thanks to [wikrie’s example](https://gist.github.com/wikrie/f1d5747a714e0a34d0582981f7cb4cfb), I ended up writing a [small Python CLI utility that takes care of the authentication and certificate upload](https://gist.github.com/shtrom/3d701d4856c9abc8c0ca53811604f27e). It should be usable as a library to build upon (particularly the authentication piece). Let me know in the comments if you did something good with it!