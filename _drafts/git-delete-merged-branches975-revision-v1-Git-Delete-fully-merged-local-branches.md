---
id: 1000
title: 'Git: Delete fully merged local branches'
date: '2023-09-22T11:49:45+10:00'
author: 'Olivier Mehani'
excerpt: "Here's a quick one-liner to clean up every local Git branch that is fully merged to main.\n\ngit branch -d $(git branch --merged main | grep -vE '(main|develop)')"
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1000'
permalink: '/?p=1000'
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