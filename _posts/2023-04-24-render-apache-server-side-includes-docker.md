---
id: 863
title: 'Render Apache Server-side Includes one last time, with Docker'
date: '2023-04-24T23:41:28+10:00'
author: 'Olivier Mehani'
excerpt: 'How to render Apache Server-side Includes into static files automatically? Decades of running Apache dave left me with a number of static sites relying on SSI-based templating. I needed a quick, and relatively accurate, way to generate truly static HTML files from my templates. I turned to a simple Docker container to do both the rendering and the dumping of the pages. Powered by Apache and Wget.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=863'
permalink: /2023/04/24/render-apache-server-side-includes-docker/
iawp_total_views:
    - '9'
activitypub_status:
    - federated
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
categories:
    - code
    - sysadmin
    - tip
tags:
    - Apache
    - Docker
    - Wget
---

I talk about restoring backups often recently. This is because the disk on my trusty bare-metal server died. This gave me the opportunity to reassess my hosting choices, and do the ground work to move from where it was to where I want it to be.

One of those changes is moving static website hosting away from a Apache HTTPd, running on an OS I administrate (read: “frequently broke”), to a more focused and [hands-off system in the cloud, AWS S3 with a CloudFront CDN](https://blog.narf.ssji.net/2023/06/11/public-website-aws-s3-cloudfront/ "Public website with S3 and CloudFront").

Unfortunately, decades of running Apache have left me with a number of static sites using some on-the-fly templating by relying on [Server-side Includes (SSI)](https://httpd.apache.org/docs/current/howto/ssi.html). Headers, footers, geeky IPv6 and last-modified tags, … none of those work with a truly static host. I needed a solution to render those snippets into full pages.

At first, I thought I’d just write a simple parser in Python. I quickly gave up on the idea, however, when I realised I used included templates with parameters. Pretty nifty stuff, but also not trivial to write a parser for.

Then I realised I already had the perfect parser: Apache. All I needed was to let it render all the pages one last time, and publish those instead! This was packed quickly with a relatively simple Docker container, and the trusty `wget`. The busy person can find a [Gist of the Dockerfile here](https://gist.github.com/shtrom/bfaac4b6d9089e24bb495f4948d1f0f0).

The key is a simple `Dockerfile` that

1. builds off an [`httpd` base](http://hub.docker.com/_/apache) (alpine, to keep the container small)
2. installs [GNU wget](https://www.gnu.org/software/wget/) (to get all the recursive capabilities)
3. enables and configure `mod_include` and `mod_negotiation`
4. creates a small `entrypoint.sh` which starts the server, and follows with a recursive `wget` to a known output directory.

```
# usage:
#
#    docker build -t ssi-extractor - < Dockerfile
#    docker run -v ./www:/usr/local/apache2/htdocs/ -v ./out:/out ssi-extractor
FROM httpd:alpine

RUN apk update \
        & apk add wget

RUN sed -i \
        -e 's/#LoadModule include_module/LoadModule include_module/' \
        -e 's/#LoadModule negotiation_module/LoadModule negotiation_module/' \
        -e 's/Options Indexes FollowSymLinks/& Includes MultiViews/' \
        -e 's/#\(Add.*shtml\)/\1/' \
        -e 's/DirectoryIndex index.html/DirectoryIndex index.shtml/' \
        /usr/local/apache2/conf/httpd.conf \
        & rm /usr/local/apache2/htdocs/index.html

RUN mkdir /out \
        & echo '#!/bin/sh' > /cmd.sh \
        & echo 'httpd-foreground &' >> /cmd.sh \
        & echo 'sleep 3; cd /out; wget -rl 0 -nH -E --accept-regex "/[^.]*(.html)?$" http://localhost/' >> /cmd.sh \
         chmod a+x /cmd.sh

CMD ["/cmd.sh"]
```

Note the `wget` incantation, which recursively fetches everything (`-r`), *ad vitam eternam* (`-l 0`), skips using the hostname when creating a directory structure (`-nH`), fixes the extensions according to served MIME type (`-E`), and only retains HTML files (`--accept-regex ...`).

```
wget -rl 0 -nH -E --accept-regex "/[^.]*(.html)?$" http://localhost/'
```

As the `usage` comment says at the top, the image build is pretty classic. Newer versions of `docker` would complain about not using `buildx`, like a caveman.

```
docker build -t ssi-extractor - < Dockerfile
```

The extraction can then be run by mounting the source directory, containing `shtml` files as a volume to `/usr/local/apache2/htdocs`, and mount another, presumably empty, output directory in `/out`. The container will do the rest.

```
docker run -v ./www:/usr/local/apache2/htdocs/ -v ./out:/out ssi-extractor
```

The `out` directory will now contain a bunch of HTML files, which hopefully are in the desired form. A few caveat are worth noting:

- Any dynamic server variable will have a pretty arbitrary value: times, dates, and last-modified tags will obviously go stale very quickly, and configuration data such as `SERVER_ADMIN` will be a default placeholder unless the `httpd.conf` is further modified to have an adequate value.
- No attempt is made to fetch error pages, though it could be easily added by, *e.g.*, creating known entry points throwing those errors, or just hitting the `ErrorDocument`s directly.

I was using those SSI mainly for templating and ease of maintenance on sites that are no longer updated and maintained for archival purposes, so losing this flexibility in favour of truly-static pages is not an issue. If the pages were still actively edited, this would probably not have been a practical approach. That said, the Docker container-based approach is sufficiently self-contained to be weaponised into a build step. All the same, I’m glad I don’t have to do that!