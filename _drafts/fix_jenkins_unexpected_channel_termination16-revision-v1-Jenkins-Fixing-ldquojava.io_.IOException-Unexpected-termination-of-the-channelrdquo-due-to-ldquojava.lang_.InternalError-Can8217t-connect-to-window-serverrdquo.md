---
id: 815
title: 'Jenkins: Fixing &ldquo;java.io.IOException: Unexpected termination of the channel&rdquo; due to &ldquo;java.lang.InternalError: Can&#8217;t connect to window server&rdquo;'
date: '2023-02-09T23:49:06+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=815'
permalink: '/?p=815'
---

Some time ago, a PPC/Mac OS X 10.5 build slave used with Jenkins started consistently failing with a <tt>java.io.IOException: Unexpected termination of the channel due</tt> error on some Jenkins slaves.

Relaunching the agent showed the reason for the error was due to a <tt>java.lang.InternalError: Can't connect to window server</tt> exception.

This was fixed, based on [some insight from StackOverflow](http://stackoverflow.com/questions/11024555/elasticsearch-java-lang-internalerror-cant-connect-to-window-server), by setting <tt>-Djava.awt.headless=true</tt> in the *Advanced/JVM Options* for this host.