---
id: 90
title: 'Balancing the last page in twocolumn LaTeX documents'
date: '2014-05-07T13:28:05+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=90'
permalink: /2014/05/07/twocolumn-balancing-latex/
iawp_total_views:
    - '28'
categories:
    - code
    - tip
tags:
    - LaTeX
---

Some publishers, particularly the IEEE, require that the columns on the last page of an article are balanced, so it looks pretty. The problem is that the break is usually needed in the middle of the bibliography, for which less layout-control is available. Fortunately, there are some specific specific solutions for various cases, and one which works for most: [flushend](http://www.ctan.org/pkg/flushend).

The [IEEEtran BibTeX style](http://www.michaelshell.org/tex/ieeetran/bibtex/) fortunately provides a specific command to break the references after a given number of entries.

```
\IEEEtraggeratref{XX}

```

In the lucky cases where the last page contains something more than the bibliography, one can fiddle with the space in which the text is laid out, and shorten it to force a column break.

```
<tt>\enlargethispage{-Xcm}</tt>
```

Problems arise when using something different than the IEEEtran BibTeX style ([including the BibLaTeX IEEE style](https://github.com/josephwright/biblatex-ieee/issues/9)), and the bibliography is such that the page that one get a chance to enlarge is not, actually, the last page.

A recent package cater for all needs: [flushend](http://www.ctan.org/pkg/flushend). Simply including it in the preamble is sufficient to make LaTeX render the last page with roughly balanced columns, regardless of their contents. Pretty neat!

```
\usepackage{flushend}
```

**Update 2016-05-09:** When using the [biblatex-ieee](http://ctan.org/pkg/biblatex-ieee) package, the last line of the last citation may be flushed too much to the left with `flushend`. Adding the `keeplastbox` option when loading the packages fixes this.

```
\usepackage[keeplastbox]{flushend}
```