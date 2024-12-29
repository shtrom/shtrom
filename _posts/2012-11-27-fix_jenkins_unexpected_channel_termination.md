---
id: 16
title: 'Jenkins: Fixing &ldquo;java.io.IOException: Unexpected termination of the channel&rdquo; due to &ldquo;java.lang.InternalError: Can&#8217;t connect to window server&rdquo;'
date: '2012-11-27T00:00:00+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://narf.jencuthbert.com/2012/11/27/fix_jenkins_unexpected_channel_termination/'
permalink: /2012/11/27/fix_jenkins_unexpected_channel_termination/
iawp_total_views:
    - '49'
categories:
    - fix
    - sysadmin
tags:
    - Java
    - Jenkins
    - 'Mac OS X'
---

Some time ago, a PPC/Mac OS X 10.5 build slave used with Jenkins started consistently failing with a <tt>java.io.IOException: Unexpected termination of the channel due</tt> error on some Jenkins slaves.

Relaunching the agent showed the reason for the error was due to a <tt>java.lang.InternalError: Can't connect to window server</tt> exception.

This was fixed, based on [some insight from StackOverflow](http://stackoverflow.com/questions/11024555/elasticsearch-java-lang-internalerror-cant-connect-to-window-server), by setting <tt>-Djava.awt.headless=true</tt> in the *Advanced/JVM Options* for this host.