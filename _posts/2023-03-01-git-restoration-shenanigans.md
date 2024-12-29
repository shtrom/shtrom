---
id: 821
title: 'Git restoration shenanigans'
date: '2023-03-01T18:30:20+11:00'
author: 'Olivier Mehani'
excerpt: 'How to fix git errors `fatal: git upload-pack: not our ref 0000000000000000000000000000000000000000` and `! [remote rejected] master -> master (missing necessary objects)`?'
layout: post
guid: 'https://blog.narf.ssji.net/?p=821'
permalink: /2023/03/01/git-restoration-shenanigans/
iawp_total_views:
    - '145'
categories:
    - fix
    - sysadmin
    - tip
tags:
    - backup
    - Git
---

Backups. What a better time to test ’em than when you need ’em. Don’t lie. I know you’ve been there too. In an unfortunate turn of events, I had to restore a number of bare git repos from recent off-site copies (made with the handy [rdiff-backup](https://rdiff-backup.net/)), but they needed a bit more work to be functional.

Once restored, I couldn’t `pull` or `push` from my existing working copies. I was greeted with [cryptic error messages instead](#cryptic-error-messages): `fatal: git upload-pack: not our ref 0000000000000000000000000000000000000000` and `! [remote rejected] master -> master (missing necessary objects)`, respectively.

No amount of searching led to an adequate solution. So I simply leveraged git’s distributedness, and used one of the clone to recreate my bare repo. I was nonetheless a bit worried about having lost a few commits on the tip.

[Playing in the bare repo later on led me to a more satisfying solution](#fixing-bare-repo). Apparently, the `refs/heads/master` file was corrupted (empty), and editing it to contain the full `sha-1` of the tip was enough to fix the issue. I found the `sha-1` of the desired commit in the `packed-refs` file at the root of the bare repo. Once done, everything worked as before, and pre-existing working copies were able to `pull` and `push` without issue.

I learned two things:

- A bit more about git
- That I didn’t actually have any more commits there

Backups! Yay!

## Cryptic error messages

```
working-copy$ <strong>git pull</strong>
fatal: git upload-pack: not our ref 0000000000000000000000000000000000000000
fatal: unable to write to remote: Broken pipe
working-copy$ <strong>git push</strong>

Enumerating objects: 98, done.
Counting objects: 100% (98/98), done.
Delta compression using up to 2 threads
Compressing objects: 100% (92/92), done.
Writing objects: 100% (92/92), 27.87 KiB | 951.00 KiB/s, done.
Total 92 (delta 62), reused 0 (delta 0), pack-reused 0
remote: fatal: bad object refs/heads/master
fatal: bad object refs/heads/master
To remote:bare-repo
 ! [remote rejected] master -> master (missing necessary objects)
error: failed to push some refs to 'remote:bare-repo'
```

## Fixing the bare repo

```
bare-repo.git$ <strong>git log</strong>
fatal: your current branch appears to be broken
bare-repo.git$ <strong>cat HEAD</strong>
ref: refs/heads/master
bare-repo.git$ <strong>cat refs/heads/master</strong>
bare-repo.git$ <strong>cat packed-refs</strong>
# pack-refs with: peeled fully-peeled sorted 
8fe5cdc45f8b35044da5a431369bc313411fbfd4 refs/heads/install_rtm
fe7020ffe89e34f57d2f8d680e727e6ef03593b6 refs/heads/master
bare-repo.git$ <strong>echo fe7020ffe89e34f57d2f8d680e727e6ef03593b6 > refs/heads/master</strong>
bace-repo.git$ <strong>git log</strong>
# Now works!
```