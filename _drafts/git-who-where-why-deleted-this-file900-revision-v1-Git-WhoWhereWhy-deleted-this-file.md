---
id: 1704
title: 'Git: Who/Where/Why deleted this file?'
date: '2024-10-31T16:57:55+11:00'
author: 'Olivier Mehani'
excerpt: "Have you ever wondered when your favourite file was deleted from a git repo? You can't git blame a file that's no longer there, but you can bisect to find the first revision where your file disappeared:\n$ git bisect run sh -c \"git ls-tree --name-only HEAD | grep ^[FILENAME]$\""
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1704'
permalink: '/?p=1704'
footnotes:
    - ''
---

Have you ever wondered when your favourite file was deleted from a git repo? No luck there, you can’t git blame a file that’s no longer there! But [you can bisect to find the first revision where your file disappeared](https://www.git-scm.com/docs/git-bisect), using [git ls-tree](https://www.git-scm.com/docs/git-ls-tree) to check for the file presence in each commit.

tl;dr:

```
$ git bisect run sh -c "git ls-tree --name-only HEAD | grep ^[FILENAME]$"
```

As a example, we have a project to catalogue all letters, one (empty) file each. We already added a few

```
~/a-void$ <strong>git log --oneline</strong>
7962f0e (HEAD -> master) Wait.
3bdb5fc Lucky the number of letters is finite
8076d7e Even more letters
c4019e4 More letters
21fccff Some letters
~/a-void$ <strong>ls</strong>
a  b  c  d  é  f  g  h  i  j  k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z
```

But wait. What is it with `é`, and where is `e`. What happened? Let’s investigate!

We can easily tell where `é` came from with a simple `<a href="https://www.git-scm.com/docs/git-log" title="">git log</a>`.

```
~/a-void$ <strong>git log é</strong>
commit 7962f0ef5cb8b949cb16f541b68bd7fe4cf8e72a (HEAD -> master)
Author: Olivier Mehani <shtrom@ssji.net>
Date:   Thu Oct 31 16:18:35 2024 +1100

    Wait.
```

We can use some [git plumbing commands](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain) (in this case `<a href="https://www.git-scm.com/docs/git-ls-tree" title="">git ls-tree</a>` to inspect the trees, and a simple grep will tell us whether the file is present or not.

```
~/a-void$ <strong>git ls-tree --name-only HEAD | grep ^e$ || echo GONE</strong>
GONE
```

But it WAS ‘ere 4 commits ago.

```
~/a-void$ <strong>git ls-tree --name-only HEAD~4 | grep ^e$ || echo GONE</strong>
e
```

So we can use `git bisect` to trawl through the list of commits, and find the first one where it’s gone. We start by stating what we know about which commit is good, and which isn’t (`new` and `old` can be used as alternatives for `bad` and `good`).

```
~/a-void$ <strong>git bisect bad</strong>
You need to start by "git bisect start"

Do you want me to do it for you [Y/n]? <strong>y</strong>
status: waiting for both good and bad commits
status: waiting for good commit(s), bad commit known
~/a-void$ <strong>git bisect good HEAD~4</strong>
Bisecting: 1 revision left to test after this (roughly 1 step)
[8076d7ec318ed717c5e351e3b47cc2dbf8d53653] Even more letters
```

Then we let `git bisect` run the script on all commits (well, not all, because it’s smart and halves the search space on every iteration). Note that despite there being 4 commits, only “roughly 1 step” will be needed to find the bad commit, rather than inspect every single one until it’s found.

```
~/a-void$ <strong>git bisect run sh -c "git ls-tree --name-only HEAD | grep ^e$"</strong>
running 'sh' '-c' 'git ls-tree --name-only HEAD | grep ^e$'
Bisecting: 0 revisions left to test after this (roughly 0 steps)
[c4019e43404882b050e9480eb75998a81991d683] More letters
running 'sh' '-c' 'git ls-tree --name-only HEAD | grep ^e$'
c4019e43404882b050e9480eb75998a81991d683 is the first bad commit
commit c4019e43404882b050e9480eb75998a81991d683
Author: Olivier Mehani <shtrom@ssji.net>
Date:   Thu Oct 31 16:17:16 2024 +1100

    More letters

 e => f | 0
 g      | 0
 h      | 0
 i      | 0
 j      | 0
 5 files changed, 0 insertions(+), 0 deletions(-)
 rename e => f (100%)
 create mode 100644 g
 create mode 100644 h
 create mode 100644 i
 create mode 100644 j
bisect found first bad commit
```

And here we are! The first bad commit was found, after 2 steps. It looks like… someone… deleted the all important letter `e` when adding the following batch. How careless!