---
id: 1060
title: 'git commit &#8211;fixup :/'
date: '2023-11-13T23:39:24+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1060'
permalink: '/?p=1060'
---

I recently happened upon an article by [Julia Evans](https://jvns.ca/)

https://jvns.ca/blog/2023/11/06/rebasing-what-can-go-wrong-/

you can use `:/` to find the ID of the most recent commit (not necessarily on your current branch) with message containing “.

It’s a killer feature with `–fixup` and `–squash`. This allows you to create fixes to past commits that 1. you only vaguely remember the message of, and 2. Git can automatically move (autosquash) in the next interactive rebase.

For example `git commit –fixup “:/hat feat”` may create a `!fixup That feature` commit.

<figure class="wp-block-video wp-block-embed is-type-video is-provider-videopress"><div class="wp-block-embed__wrapper"><iframe allow="clipboard-write" allowfullscreen="" aria-label="VideoPress Video Player" data-resize-to-parent="true" frameborder="0" height="615" src="https://videopress.com/embed/tNvKsiuZ?cover=1&preloadContent=metadata&useAverageColor=1&hd=0" title="VideoPress Video Player" width="770"></iframe><script src="https://v0.wordpress.com/js/next/videopress-iframe.js?m=1725245713"></script></div></figure>