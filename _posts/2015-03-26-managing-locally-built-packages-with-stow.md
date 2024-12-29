---
id: 127
title: 'Managing locally-built packages without wrecking the system, with stow(8)'
date: '2015-03-26T22:53:52+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=127'
permalink: /2015/03/26/managing-locally-built-packages-with-stow/
iawp_total_views:
    - '2'
categories:
    - rant
    - sysadmin
    - tip
tags:
    - stow
    - Unix
---

It is bad practice to use `make install`. Period.

Why? Because it installs files everywhere on your system—if you’re lucky, only in `/usr/local`—with no guaranteed way to cleanly remove them afterwards.

Yet, sometimes, there is no other option, for example if some software is not packaged for your Unix of choice and you don’t have time to do it yourself. There are some easy and rather straightforward ways around it, which I usually recommend to beginners.

It happened again today. So I recommended the use of `/opt/PKG-VER` as an installation prefix and [stow(8)](https://www.gnu.org/software/stow/) to make the software seamlessly available to the rest of the system. Nothing fancy or novel, but I thought I’d share the summary email in the hope it would help others.

My email read as follows.

> First of all, never do a bare `make install`. Always install to a directory specific to your software. `/opt` is rather standard base path, and this can be told to `make` with variables such as `PREFIX` or `DESTDIR` (though you might need to look into the `Makefile` or documentation to find if it is different). Try a non-root run first to make sure it tries to install in the right place.
> 
> ```
> sudo make PREFIX=/opt/PKG-VER install
> ```
> 
> Then, your package is in `$PREFIX`, with the normal directory layout, but the system can’t see it because it is not in its usual paths. You can create symlinks to all the files in your package in the usual system paths using `<a href="http://linux.die.net/man/8/stow">stow</a>`(8).
> 
> ```
> stow -d /opt/ -t /usr/local/ PKG-VER
> ```
> 
> You can use -n to do a dry run to make sure it does what you want first. Removing the symlinks is equally easy.
> 
> ```
> sudo stow -D -d /opt -t /usr/local/ PKG-VER
> ```
> 
> As an added bonus: de-installing (well, deleting) files from a previous `make install` without `PREFIX`. You need to have another copy of the installed layout, this time done with the `PREFIX`
> 
> ```
> cd $PREFIX
> find -type f -exec echo rm /usr/local/{} \; # Double check that we will only remove what we want
> sudo find -type f -exec rm /usr/local/{} \; # Do it for real
> ```
> 
> Note the `-type f` option to `<a href="http://linux.die.net/man/1/find">find</a>`(1), which tells it to only work on files, and not directories. Otherwise, you might end up removing things such as `/usr/local/lib` (particularly if you used `rm -rf`), and it will be painful.