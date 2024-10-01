---
id: 1671
title: '`grep`ping your `tty` and showing it too'
date: '2024-08-28T17:28:40+10:00'
author: 'Olivier Mehani'
excerpt: 'How would one inspect the output of a program AND display it, but without temporary files or variables? tl;dr: Use  tee(1) to duplicate  stdout to /dev/tty, and allow it to be processed by grep.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1671'
permalink: /2024/08/28/grepping-your-tty-and-showing-it-too/
activitypub_status:
    - federated
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '2'
categories:
    - code
    - oneliner
    - sysadmin
    - tip
tags:
    - Linux
    - 'Mac OS X'
    - shell
---

How would one inspect the output of a program AND display it. My general approach is to use variables or temporary files, but are there other options?

Recently, I was writing a test automation script. I was working with an uncooperative program (looking at you, `aws sam local`), that would happily output errors on its output stream, but always terminate with a successful status code. For the sake of the automation, I needed to find occurrences of an error string in the output of the program. `grep` of course is the tool of choice, but it would only print that line, or remove it with `-v`, which would make visual inspection by a human more difficult.

tl;dr: Use [`tee`(1)](https://www.man7.org/linux/man-pages/man1/tee.1.html) to duplicate `stdout` to `/dev/tty`, and allow it to be processed by `grep`.

My first thought was that I needed to duplicate the output, allow on copy to be printed verbatim, and the other one to be parsed as needed. `tee` is a perfect tool to duplicate a stream to a file, while `grep` can process the other copy.

```
$ echo -e 'a\nb' | tee out | grep -qn a && echo a was found 
a was found
$ cat out
a
b
$ rm out
```

This is almost the solution I’m after, but it relies on a temporary file which needs to be cleaned up.

Fortunately, there is a special device file, `/dev/tty` (on Linux and Darwin, at least), which corresponds to the current console. Writing to this file \_looks\_ the same as directly outputing to the local terminal.

```
$ echo I am stdout
I am stdout
$ echo I am /dev/tty > /dev/tty
I am /dev/tty
```

Putting those two bricks together, `tee` can be used to duplicate the string to the `/dev/tty` file, which will result is the raw content being output back onto the current terminal, while `grep` can silently check whether a desired string is present (or not).

```
$ echo -e 'a\nb' | tee /dev/tty
a
b
a
b
$ echo -e 'a\nb' | tee /dev/tty | grep -qn a && echo a was found
a
b
a was found
```

Using this construct, I could run a local instance of an AWS Lambda function with SAM, and detect any error that would otherwise be output in the logs. This allowed me to have a much quicker test-fail-fast-debug loop, rather than having to upload buggy code to the cloud and wait for the logs to become available.