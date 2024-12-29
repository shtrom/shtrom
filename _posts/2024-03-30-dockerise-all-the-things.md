---
id: 1372
title: 'Dockerise all the things!'
date: '2024-03-30T00:56:33+11:00'
author: 'Olivier Mehani'
excerpt: 'I''ve been trying to run everything in Docker. It''s particularly useful for random codebases. It is handy to quickly provide the needed dependencies without having to make long-term changes to my system. It is relatively simple, and only needs slight variations on a very basic Dockerfile.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1372'
permalink: /2024/03/30/dockerise-all-the-things/
activitypub_status:
    - federated
iawp_total_views:
    - '5'
image: /wp-content/uploads/sites/3/2024/03/image-3.png
categories:
    - code
    - sysadmin
    - tip
tags:
    - Docker
---

Recently, I’ve been trying to run everything I need to test in Docker. It’s particularly useful for random codebases I try out, to quickly provide the needed dependencies without having to make long-term changes to my system. It also provides some amount of isolation and segregation for applications of unclear origin.

Doing so is relatively simple, and only needs slight variations on a very basic Dockerfile, e.g.,

```
FROM RUNTIME

COPY . /app

ENTRYPOINT ["/app/CMD_FROM_README"]
```

Using an `ENTRYPOINT` allows Docker to pass additional command line arguments to the `CMD_FROM_README`.

Here’s a full example for a Python application.

```
FROM python

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN manage.py migrate

EXPOSE 8001

ENTRYPOINT ["python", "manage.py"]

CMD ["runserver", "8001"]
```

(The `CMD` here gives the default arguments to the `ENTRYPOINT`, but will get overridden by anything you give on the command line).

You can then build with

```
docker build . -t IMAGENAME
```

and run using the name you just gave the image, e.g.,

```
docker run -it IMAGENAME --help
```

(note that the `--help` here will replace the `CMD` that gets passed to the `ENTRYPOINT`).

This works for both server applications, like the previous example, which `EXPOSE` a service over a network port, as well as for simpler command line applications.

One caveat is that input/output with containerised command line tools needs to happen via `stdin`/`stdout`. Some applications don’t natively support this, and instead expect files to be reachable via the filesystem. A workaround is to write a small `ENTRYPOINT` script that reads `stdin` and writes it to a file in the container before calling the application on this file.

A simple entrypoint is as follows.

```
#!/bin/sh -x
cat >/tmp/in

tac "$@" /tmp/in
```

It uses `cat` to capture the standard input to the container into a temporary file, then call the command (here, [`tac(1)`, which simply reverses the order of the input lines](https://www.man7.org/linux/man-pages/man1/tac.1.html)) on the file. Passing `"$@"` to the command allows the `ENTRYPOINT` to continue parsing the rest of the command line arguments.

<div class="wp-block-image"><figure class="aligncenter size-full wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd76bcf"}" data-wp-interactive="core/image">![Screenshot showing a docker build and subsequent use of the container to process stdin without and with additional arguments on the command line.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/image-3.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screenshot showing a docker build and subsequent use of the container to process stdin without and with additional arguments on the command line." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></div>For more complex setups, e.g., more than one file, it is also possible to mount the input and output files using `--volume` arguments, and letting either the `ENTRYPOINT` or the `CMD` reference those files. It however makes the command line more complex and less straightforward.

```
docker run -v ./in1:/in1 -v ./in2:/in2 -v ./out:/out tac
```

<div class="wp-block-image"><figure class="aligncenter size-full">![Screenshot showing a docker build and subsequent use of the container to process multiple input files via bind volume mounts.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/image-1.png)</figure></div>