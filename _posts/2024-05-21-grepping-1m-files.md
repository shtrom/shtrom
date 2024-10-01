---
id: 1552
title: 'grepping 1M+ files'
date: '2024-05-21T12:29:27+10:00'
author: 'Olivier Mehani'
excerpt: 'I have a directory with a lot (~1M) of files to `grep` through. But it''s too much and raises an `Argument list too long` error. A combination of `xargs` and `getconf` can be used to scale up the command: `ls | xargs -n $(($(getconf ARG_MAX))) grep HTTP.*200`.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1552'
permalink: /2024/05/21/grepping-1m-files/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
iawp_total_views:
    - '10'
footnotes:
    - ''
image: /wp-content/uploads/sites/3/2024/05/Screenshot-2024-05-21-at-17.21.16-e1716276848337.png
categories:
    - sysadmin
    - tip
tags:
    - Linux
    - shell
    - Unix
---

So, I have a directory with a lot (~1M) of files (HTTP responses). I need to filter them based on contents (successful responses). Unfortunately, the simple solution

```
grep HTTP.*200 *
```

doesn’t work

```
-bash: /usr/bin/grep: Argument list too long
```

So some more shell pipelining is needed to solve the problem.

tl;dr:

- `<a href="https://www.man7.org/linux/man-pages/man1/xargs.1.html">xargs(1)</a>` can be used to split the argument list and run parallel processes
- `<a href="https://www.man7.org/linux/man-pages/man1/getconf.1p.html">getconf(1p)</a>` can get the value of system variable, such as `ARG_MAX`
- so, `ls | xargs -n $(getconf ARG_MAX) grep HTTP.*200` is what I need.

`xargs` can slice a list of the arguments to pass to grep, with `-n <ARG_COUNT>`. But what value do I give for `ARG_COUNT`? Thanks to [this article](https://www.cyberciti.biz/faq/argument-list-too-long-error-solution/), I discovered a handy command, `getconf`, which can read the `ARG_MAX` value. <s>It also seems like `xargs` is able to account for static parameters to the command, and make the dynamic argument list short enough to not trip over the limit.</s>

`xargs` can also run multiple processes in parallel with the `-P` option. Let’s run one per CPU. Under Linux, one way to get the CPU count is by counting the number of entries in `/proc/cpuinfo`. This can be done with `grep -c processor /proc/cpuinfo`.

And here’s our final command line, which

1. slices the file list in batches of `ARG_MAX`,
2. runs as many parallel `grep` processes as the number of CPUs on the box,
3. outputs matches prefixed with filenames (thanks to the `-H` flag to `grep`), and
4. also appends the output to a log file, named after the current directory, using [`tee`(1)](https://www.man7.org/linux/man-pages/man1/tee.1.html):

```
ls \<br></br>  | xargs \<br></br>    -n $(($(getconf ARG_MAX))) \<br></br>    -P $(grep -c processor /proc/cpuinfo) \<br></br>    grep HTTP.*200 \<br></br>  | tee -a ../$(basename $(pwd)).log<br></br>
```

# Erratum

Now, this all works pretty nicely, but I realised when discussing with [a colleague, already (in)famous here](/2022/11/27/the-ultimate-bash-startup-logic/#zsh "The ultimate bash startup logic"), that the explanation above is not quite right: while `-n <ARG_COUNT>` limits the number of arguments, `ARG_MAX` is more than 2.5M, so `grep` shouldn’t have had an issue fitting those ~1M arguments.

According [`sysconf`(3)](https://www.man7.org/linux/man-pages/man3/sysconf.3.html), `ARG_MAX` is actually the maximum *length* of all the arguments. So 1M 6-digit file names certainly exceed 2.5MiB. What is happening here? Well, it seems like, when using the `-n `option, `xargs` automatically adjusts the length of the line to fit within the alloted buffer space.

<figure class="wp-block-image aligncenter size-full">![Excerpt from the xargs(1) manpage: 

       -n max-args, --max-args=max-args
              Use at most max-args arguments per command line.  Fewer than max-args arguments will be used if the size (see  the  -s
              option) is exceeded, unless the -x option is given, in which case xargs will exit.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/05/Screenshot-2024-05-21-at-17.21.16.png)</figure>This can be confirmed by passing the `-x` option which, according to the documentation for the `-n` flag, should force an exit in error, rather than a slower-with-more-processes success. And sure enough,

<div class="wp-block-image"><figure class="aligncenter size-full">![Screenshot of running xargs with -x. $ ls | xargs -x -n $(getconf ARG_MAX) grep HTTP.*200 >/dev/null xargs: argument list too long](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/05/Screenshot-2024-05-21-at-17.29.20.png)</figure></div>So, this all still works as desired, but not for the reasons that led to this solution.