---
id: 1011
title: 'Git: fixup a commit by message'
date: '2023-11-14T00:07:18+11:00'
author: 'Olivier Mehani'
excerpt: 'git commit supports --fixup|--squash <commitid> to create a commit that can be automatically squashed. You can use :/<RegExp> to resolve a regular expression to the id of a matching commit. This will find the ID of the most recent commit with message matching /<RegExp>/ and resolve to that.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1011'
permalink: /2023/11/14/git-fixup-a-commit-by-message/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
image: /wp-content/uploads/sites/3/2023/11/git-rebase-interactive.jpg
categories:
    - tip
tags:
    - Git
---

I recently happened upon an article by [Julia Evans](https://jvns.ca/) on [what can go wrong when rebasing in Git](https://jvns.ca/blog/2023/11/06/rebasing-what-can-go-wrong-/). This made me realise that I should probably talk about my favourite, yet obscure, Git feature.

When using `commit` you can use [`--fixup` &lt;commitid&gt;](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---fixupamendrewordltcommitgt) or [`--squash` &lt;commitid&gt;](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---fixupamendrewordltcommitgt) to create a commit that can be automatically fixup’d or squashed on the next [`rebase` with `--autosquash`](https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt---autosquash). This is handy, but you need to know the `commitid` beforehand.

There is a type of [`refspec` that can resolve a regular expression to the `commitid` of a matching commit: `:/<RegExp>`](https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt-emlttextgtemegemfixnastybugem). This will find the ID of the most recent commit (not necessarily on your current branch) with message matching `/<RegExp>/`, and resolve to that.

It’s a killer feature with `--fixup` and `--squash`: in a pinch, you can create fixes to past commits that

1. you only vaguely remember the message of, and
2. Git can automatically move (autosquash) in the next interactive rebase.

For example `git commit --fixup ":/hat feat"` may create a `!fixup That feature` commit. The `!fixup` prefix is what `--autosquash` uses to reorder commits.

Here’s a quick video example.

<figure class="wp-block-video"><video controls="" poster="https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/git_commit-fixup_avi_std.original.jpg" src="https://blog.narf.ssji.net/git_commit-fixup-avi/"></video></figure>