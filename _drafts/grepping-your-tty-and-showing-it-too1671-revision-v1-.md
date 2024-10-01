---
id: 1673
date: '2024-08-22T15:23:30+10:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1673'
permalink: '/?p=1673'
---

If you want to both show AND parse some output, you can generally use tee to duplicate the stream to a file. But what if you don’t want a temporary file?Well, you can output to /dev/tty, which is your current terminal, so you get a duplicated stream shown.But you only still have one set of data being passed via stdout, so you can build your pipeline on this.  
  
  
\[15:22:58\] ~/work$ echo -e ‘a\\nb’ | tee /dev/tty <staging>  
a  
b  
a  
b  
  
  
\[15:23:07\] ~/work$ echo -e ‘a\\nb’ | tee /dev/tty | grep -qn a &amp;&amp; echo a was found <staging>  
a  
b  
a was found</staging></staging>