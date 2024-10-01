---
id: 975
title: 'Git: Delete fully merged local branches'
date: '2023-09-14T17:17:47+10:00'
author: 'Olivier Mehani'
excerpt: "Here's a quick one-liner to clean up every local Git branch that is fully merged to main.\n\ngit branch -d $(git branch --merged main | grep -vE '(main|develop)')"
layout: post
guid: 'https://blog.narf.ssji.net/?p=975'
permalink: /2023/09/14/git-delete-merged-branches/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
footnotes:
    - ''
categories:
    - oneliner
    - tip
tags:
    - Git
    - shell
---

When working on many feature branches, they tend to accumulate in the local Git clone. Even if they get deleted in upstream shared repos, they need to be cleared locally, too, otherwise they will stick around forever.

Here’s a quick one-liner to clean up every branch that is fully merged to `main`. It does make sure not to delete `main` and `develop`, though.

```
git branch -d $(git branch --merged main | grep -vE '(^\*|master|main|develop)')

```

Update (2029-09-22): Let’s make it a `git` alias!

```
git config --global alias.prune-merged '!f() { git branch --merged "${1}" | grep -vE "(^\*|master|main|develop)" | xargs git branch -d ; }; f'
```