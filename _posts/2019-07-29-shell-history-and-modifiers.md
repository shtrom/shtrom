---
id: 435
title: 'Shell history and modifiers'
date: '2019-07-29T14:07:41+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=435'
permalink: /2019/07/29/shell-history-and-modifiers/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
categories:
    - code
    - oneliner
    - tip
tags:
    - Bash
    - history
    - Readline
    - shell
    - Unix
    - zsh
---

I finally mastered the shell (beit bash or zsh, but really, this is [readline](https://linux.die.net/man/3/readline))’s history with command replacement. It took me 19 years and my entire family fortune to gather enough wits to read [that part of the manual](https://linux.die.net/man/3/history) with enough attention and will as to learn to use it.

Essentially, you can recall previous commands from the history with `!number`. You can then *change* some content of the previous command <span class="result__url__full">programmatically</span> before running it by adding `:s/PATTERN/REPLACEMENT/` or `:gs/PATTERN/REPLACEMENT/` (the first one will replace the first occurrence, the second one will replace them all).

So, without further ado,

```
$ echo aaa bbb aaa      # original command<br></br>aaa bbb aaa<br></br>$ history | tail  -n 1  # get the number of that last command in the history<br></br>  970  echo aaa bbb aaa<br></br>$ !970:s/aaa/ccc        # ask the shell to replay it, replacing the first occurrence of `aaa` with `ccc`<br></br>$ echo ccc bbb aaa      # the shell (zsh) put that here for me<br></br>ccc bbb aaa<br></br>$ history | tail  -n 2  # look at the history now<br></br>  970  echo aaa bbb aaa<br></br>  972  echo ccc bbb aaa<br></br>$ !970:gs/aaa/ccc       # now replace all occurrences of `aaa` with `ccc`<br></br>$ echo ccc bbb ccc      # thanks, shell<br></br>ccc bbb ccc
```

I’ve always triggered that behaviour by mistake, and my fingers would never fall in the right way when I needed it before. Those times are gone!

As I pointed this out at work, Scott Hugues further elaborated that you can also do this much faster if you want to reuse a version of the last command you ran.

```
$ echo aaa<br></br>aaa<br></br>$ ^aaa^bbb<br></br>echo bbb<br></br>bbb
```

Good times.