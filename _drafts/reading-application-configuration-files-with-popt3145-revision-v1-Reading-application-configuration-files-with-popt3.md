---
id: 799
title: 'Reading application configuration files with popt(3)'
date: '2023-02-09T23:48:45+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=799'
permalink: '/?p=799'
---

[Popt](http://www.freecode.com/projects/popt/) has a [poptReadConfigFile()](http://linux.die.net/man/3/popt) which is described as doing the following

> ```
>  The file specified by fn is opened and parsed as a popt configuration file. This allows programs to use program-specific configuration files.
> ```

What’s unclear is whether it can only be used to enable aliases, or if it can also be used as a general-purpose configuration file to replace the command-line interface, and if so, what format it should be in.

As no documentation I could find explains it one way or the other, I resorted to reading the code.

The short answer is no. **Popt (1.16) cannot read command line parameters from an rc configuration file.**

There is an undocumented feature of the popt configuration file parsing, `exec`s, which I hope would serve my purpose, but this is unfortunately not the case. Rather, they allow the execution of other binaries when specific options are seen.

For the sake of completeness, here is an example of the configuration syntax for both `alias`es and `exec`s. [The popt source tree also ships with some examples](http://rpm5.org/cvs/fileview?f=popt/test-poptrc).

> ```
> PROGRAM alias --NEWOPT1 --OLDOPT1 --OLDOPT2=VAL2
> PROGRAM alias --NEWOPT2 OTHER-PROGRAM
> ```

With this configuration file as, e.g., `~/.poptrc`, `PROGRAM` will behave as follows.

- `PROGRAM --NEWOPT1` will behave as if `PROGRAM --OLDOPT1 --OLDOPT2=VAL2` had been called;
- `PROGRAM --NEWOPT2` will [exec](http://linux.die.net/man/3/exec)(3) `OTHER-PROGRAM`, and terminate when it does.

I’m not quite sure I understand the point of `exec`s…