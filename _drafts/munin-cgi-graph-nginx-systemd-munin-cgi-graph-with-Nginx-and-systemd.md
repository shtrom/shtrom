---
id: 259
title: 'munin-cgi-graph with Nginx and systemd'
date: '2024-01-05T09:37:17+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=259'
permalink: '/?p=259'
categories:
    - sysadmin
    - tip
tags:
    - Debian
    - FastCGI
    - Linux
    - Munin
    - munin-cgi-graph
    - nginx
    - spawn-fcgi
    - systemd
    - Unix
    - wip
---

> [SystemD FastCGI multiple processes](https://nileshgr.com/2016/07/09/systemd-fastcgi-multiple-processes/)

<iframe class="wp-embedded-content" data-secret="uXqbs7XXEb" frameborder="0" height="338" loading="lazy" marginheight="0" marginwidth="0" sandbox="allow-scripts" scrolling="no" security="restricted" src="https://nileshgr.com/2016/07/09/systemd-fastcgi-multiple-processes/embed/#?secret=wlfzNcEXL0#?secret=uXqbs7XXEb" style="position: absolute; visibility: hidden;" title="“SystemD FastCGI multiple processes” — NileshGR" width="600"></iframe>

Old way: spawn-fcgi

```
$ cat /etc/systemd/system/munin-cgi-graph-fcgi.service
[Unit]
Description = Munin Graph FastCGI backend

[Service]
User = munin
Group = munin
ExecStart = /usr/lib/munin/cgi/munin-cgi-graph
StandardOutput = null
StandardInput = socket
StandardError = null
Restart = always

[Install]
WantedBy = multi-user.target
$ cat /etc/systemd/system/munin-cgi-graph-fcgi.socket
[Unit]
Description = Munin Graph FastCGI Socket

[Socket]
SocketUser = www-data
SocketGroup = www-data
SocketMode = 0660
ListenStream = /var/run/munin/munin-fastcgi-graph.sock

[Install]
WantedBy = sockets.target
$ sudo systemctl enable /etc/systemd/system/munin-cgi-graph-fcgi.service /etc/systemd/system/munin-cgi-graph-fcgi.socket
```

Nginx config:

```
        location /munin-cgi/munin-cgi-graph/ {
                fastcgi_split_path_info ^(/munin-cgi/munin-cgi-graph)(.*);
                fastcgi_param PATH_INFO $fastcgi_path_info;
                fastcgi_pass unix:/var/run/munin/munin-fastcgi-graph.sock;
                include fastcgi_params;
        }
```

Single-process limitations and workaround: https://nileshgr.com/2016/07/09/systemd-fastcgi-multiple-processes