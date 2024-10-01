---
id: 1680
title: 'Moving subset of git repository while retaining history'
date: '2024-09-02T16:01:35+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1680'
permalink: '/?p=1680'
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
categories:
    - Uncategorised
---

git filter-branch -f –subdirectory-filter www/demos/hack2018/cqt-blockly –index-filter \\  
‘git ls-files -s | sed “s@\\t\\”\*@&amp;www/staff/omehani/cqt-blockly/@” |  
GIT\_INDEX\_FILE=$GIT\_INDEX\_FILE.new \\  
git update-index –index-info &amp;&amp;  
mv “$GIT\_INDEX\_FILE.new” “$GIT\_INDEX\_FILE”‘ HEAD

initial\_commit\_id=$(git log –reverse | sed -n ‘s/commit //p;q’)

git show ${initial\_commit\_id} &gt; 000.patch # didn’t work for me

git format-patch ${initial\_commit\_id}

git am ../site-docs/\*.patch # also didn’t work after a while