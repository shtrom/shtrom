---
id: 216
title: 'Security considerations and Building Trust'
date: '2016-02-10T10:34:34+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=216'
permalink: /2016/02/10/security-considerations-and-building-trust/
enclosure:
    - "http://blog.narf.ssji.net/wp-content/uploads/sites/3/2016/02/2015-09-10mehani_security_considerations_building_trust.webm\n104798430\nvideo/webm\n"
image: /wp-content/uploads/sites/3/2016/02/Screenshot-from-2018-02-13-15-47-14.png
categories:
    - presentation
    - security
    - Sydney
    - tip
tags:
    - CAcert
    - 'Certificate Authorities'
    - cryptography
    - ffmpeg
    - 'Free Software Sydney'
    - hash
    - 'Let''s Encrypt'
    - PGP
    - 'reproducible builds'
    - SSL
---

In September last year, the [Free Software Sydney meet-up group](http://freesoftware.org.au/sydney/) had an inaugural [Jitsi Meet](http://meet.jitsi.org/) videoconference.

My (longer-than-planned) contribution to the conference aimed at introducing trust and security concepts, mainly in showing the prevalent role of hashes, and covered public-key cryptography uses, GPG, SSL CAs, trusting trust and reproducible builds.

<figure class="wp-block-video"><video controls="" src="https://blog.narf.ssji.net/wp-content/uploads/sites/3/2016/02/2015-09-10mehani_security_considerations_building_trust.webm"></video></figure>The whole video of the conference, also covering Free Software and Tor, can be found on [the page of the event](http://freesoftware.org.au/sydney/2015-09-10-lets-free-sydney/past-events/2015-09-10-lets-free-sydney/). [PDF slides are available here](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2016/02/2015-09-10mehani_trust.pdf).

As a side note, thanks to [this post](https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video#704118), here’s a quick way to extract a clip off a longer video with `ffmpeg`. I did however have to fiddle with the time to seek to, and ended up seeking to about 10 minutes before the actual time of the beginning of the segment.````

```
ffmpeg -ss 00:10:00 -i Free_Software_Sydney_Web_Conference_September_2015-BJ0Y9YVRg3A.medium.webm -ss 00:13:23 -t 00:56:16 -c copy 2015-09-10mehani_security_considerations_building_trust.webm
```