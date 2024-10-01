---
id: 27
title: 'Who are all the authors of this function?'
date: '2013-10-11T00:00:00+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://narf.jencuthbert.com/2013/10/11/git-function-authors/'
permalink: /2013/10/11/git-function-authors/
categories:
    - tip
tags:
    - Git
---

<tt><span style="font-variant: small-caps">g</span>it</tt> has many useful features in [<tt>git log</tt>(1)](http://git-scm.com/docs/git-log) and [<tt>git blame</tt>(1)](http://git-scm.com/docs/git-blame) to display the history of a file, or who contributed each line in said file, respectively. However, it might be useful to get the full history not of a file or a line but, say, a function (that is, more than one line in a coherent structure). This can be interesting for things such as displaying all the authors of a given function.

Of course, <tt>git</tt> can do this. Both commands cited above have an almost similar <tt>-L</tt> option which allows to work only on a subset of lines. An interesting way of expressing this subset is with the <tt>:&lt;regexp&gt;</tt> construct. It instructs <tt>git</tt> to find <tt>funcname</tt>s matching that regular expression, and consider the lines following until a new <tt>funcname</tt> is found (I haven’t found much documentation on what <tt>funcname</tt> is, but presumably, this is what <tt>git</tt> uses to identify functions in a particulary source language to give context in diff outputs). <tt>git log</tt> has an additional expectation after the regexp: the name of a file in which to find matching <tt>funcname</tt>s, separated from the regexp by a colon.

I initially thought that <tt>git blame</tt> would be the tool, but it turns out that <tt>git log</tt> is better armed. Unfortunately, it also outputs the diff with every commit, which is more than we need in that case, even with custom formats, so we need to do some plumbing.

```
shtrom@lxiv:~/nicta/OML/oml (staging)$ git log   -L :omlc_inject:lib/client/api.c   --format="Author: %aN" | sed -n "s/^Author: //p" | sort | uniq
Jolyon White
Olivier Mehani
```

The format simply asks each author’s name, preceded by a tag for easier extraction. We could have used <tt>git log</tt>‘- porcelain output, but it doesn’t apply the mappings in <tt>mailmap</tt> ([documented in <tt>git shortlog</tt>(1)](http://git-scm.com/docs/git-shortlog#_mapping_authors)), and might result in different versions of authors’ names, which would remain duplicated after the <tt>sort | uniq</tt> gymnastics.

A word of caution, though: as this relies on <tt>funcname</tt> to identify the beginning *and the end* of a function, the selection might extend pass the actual end of the function, and include whitespaces and top-comments for the next function. Some authors might end up being credited for working on functions they never looked at!