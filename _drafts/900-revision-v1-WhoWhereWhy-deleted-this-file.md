---
id: 903
title: 'Who/Where/Why deleted this file?'
date: '2023-05-12T10:33:49+10:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=903'
permalink: '/?p=903'
---

Have you ever wondered when your favourite file was deleted from a git repo? No luck there, you can’t git blame a file that’s no longer there!But you can git bisect https://www.git-scm.com/docs/git-bisect to find the first revision where your file was gone!As an example, we recently moved api-questions for using LDE to place the correct system-config.ini in place, to a system where they are all present in the config directory, and named after the environment they apply to (more on this here: https://learnosity.atlassian.net/wiki/spaces/DEV/pages/2144403909/Config+Files+Environment+Config#(Experimental)-Alternate-System-Config-Filename)So, where did my old system-config.ini go?It’s not here  
  
git ls-tree –name-only -r HEAD | grep ‘system-config.ini$’ || echo ‘GONE!’  
GONE!  
  
But it WAS ‘ere 100 commits ago.  
  
$ git ls-tree –name-only -r HEAD~100 | grep ‘system-config.ini$’ || echo ‘GONE!’  
lde\_config/ldc/php-fpm/system-config.ini  
lde\_config/lde/system-config.ini  
  
So we can use git bisect to trawl through the list of commits, and find the first one where it’s gone. We start by stating what we know about which commit is good, and which isn’t.  
  
$ git bisect bad HEAD  
$ git bisect good HEAD~100  
  
(You can use new and old as alternatives)Then we let git bisect run the script on all commits (well, not all, because it’s smart and halves the search space on every iteration).  
  
$ git bisect run sh -c “git ls-tree –name-only -r HEAD | grep -q ‘system-config.ini$'”  
running ‘sh’ ‘-c’ ‘git ls-tree –name-only -r HEAD | grep -q ‘\\”system-config.ini$’\\”’  
Bisecting: 67 revisions left to test after this (roughly 6 steps)  
…  
Bisecting: 0 revisions left to test after this (roughly 0 steps)  
\[1bc33434783f8a8b6d9d3a7b08da641a8426a164\] \[REFACTOR\] ENV var system config via LP  
running ‘sh’ ‘-c’ ‘git ls-tree –name-only -r HEAD | grep -q ‘\\”system-config.ini$’\\”’  
1bc33434783f8a8b6d9d3a7b08da641a8426a164 is the first bad commit  
commit 1bc33434783f8a8b6d9d3a7b08da641a8426a164  
Author: AndrewM <andrew.morrison>  
Date: Thu Apr 13 23:37:47 2023 +1000  
  
 \[REFACTOR\] ENV var system config via LP  
  
 config/system-config.ldc.ini | 122 +++++++++++++++++++++++++++++++  
 config/system-config.lde.ini | 117 +++++++++++++++++++++++++++++  
 docker-compose.yml | 2 +-  
 lde\_config/dist/api-questions-design.yml | 1 +  
 lde\_config/dist/api-questions-ldc.yml | 1 +  
 lde\_config/docker-compose.cli.yml | 2 +-  
 lde\_config/ldc/php-fpm/Dockerfile | 2 –  
 lde\_config/ldc/php-fpm/system-config.ini | 122 ——————————-  
 lde\_config/lde/system-config.ini | 117 —————————–  
 9 files changed, 243 insertions(+), 243 deletions(-)  
 create mode 100644 config/system-config.ldc.ini  
 create mode 100644 config/system-config.lde.ini  
 delete mode 100644 lde\_config/ldc/php-fpm/system-config.ini  
 delete mode 100644 lde\_config/lde/system-config.ini  
bisect found first bad commit%  
  
Ok, now we know where the file has gone! (bearbeitet)   
  
  
  
Options  
git log –stat –full-history — lde\_config/ldc/php-fpm/system-config.ini  
  
that’s the bit that confuses me. It looks like full-history limits the history pruning it does. I suspect there might be something like sorting by date rather than commit order at play.  
 vor 4 Minuten  
It include a number of seemingly unrelated merges  
 vor 3 Minuten  
with –stat, you can see the addition, change, and ultimate deletion  
  
  
https://git-scm.com/docs/git-log#Documentation/git-log.txt—grep-reflogltpatterngtWhat if you will add  
  
-g  
–walk-reflogs   
  
You’d need –walk-reflog, but I think this would only work on your local reflog, so not when someone else deleted the file, and you just pulled the changes in.  
  
for github you have access to repository reflog  
https://objectpartners.com/2014/02/11/recovering-a-commit-from-githubs-reflog/ Have you ever wondered when your favourite file was deleted from a git repo? No luck there, you can’t git blame a file that’s no longer there!But you can git bisect https://www.git-scm.com/docs/git-bisect to find the first revision where your file was gone!As an example, we recently moved api-questions for using LDE to place the correct system-config.ini in place, to a system where they are all present in the config directory, and named after the environment they apply to (more on this here: https://learnosity.atlassian.net/wiki/spaces/DEV/pages/2144403909/Config+Files+Environment+Config#(Experimental)-Alternate-System-Config-Filename)So, where did my old system-config.ini go?It’s not here  
  
git ls-tree –name-only -r HEAD | grep ‘system-config.ini$’ || echo ‘GONE!’  
GONE!  
  
But it WAS ‘ere 100 commits ago.  
  
$ git ls-tree –name-only -r HEAD~100 | grep ‘system-config.ini$’ || echo ‘GONE!’  
lde\_config/ldc/php-fpm/system-config.ini  
lde\_config/lde/system-config.ini  
  
So we can use git bisect to trawl through the list of commits, and find the first one where it’s gone. We start by stating what we know about which commit is good, and which isn’t.  
  
$ git bisect bad HEAD  
$ git bisect good HEAD~100  
  
(You can use new and old as alternatives)Then we let git bisect run the script on all commits (well, not all, because it’s smart and halves the search space on every iteration).  
  
$ git bisect run sh -c “git ls-tree –name-only -r HEAD | grep -q ‘system-config.ini$'”  
running ‘sh’ ‘-c’ ‘git ls-tree –name-only -r HEAD | grep -q ‘\\”system-config.ini$’\\”’  
Bisecting: 67 revisions left to test after this (roughly 6 steps)  
…  
Bisecting: 0 revisions left to test after this (roughly 0 steps)  
\[1bc33434783f8a8b6d9d3a7b08da641a8426a164\] \[REFACTOR\] ENV var system config via LP  
running ‘sh’ ‘-c’ ‘git ls-tree –name-only -r HEAD | grep -q ‘\\”system-config.ini$’\\”’  
1bc33434783f8a8b6d9d3a7b08da641a8426a164 is the first bad commit  
commit 1bc33434783f8a8b6d9d3a7b08da641a8426a164  
Author: AndrewM <andrew.morrison>  
Date: Thu Apr 13 23:37:47 2023 +1000  
  
 \[REFACTOR\] ENV var system config via LP  
  
 config/system-config.ldc.ini | 122 +++++++++++++++++++++++++++++++  
 config/system-config.lde.ini | 117 +++++++++++++++++++++++++++++  
 docker-compose.yml | 2 +-  
 lde\_config/dist/api-questions-design.yml | 1 +  
 lde\_config/dist/api-questions-ldc.yml | 1 +  
 lde\_config/docker-compose.cli.yml | 2 +-  
 lde\_config/ldc/php-fpm/Dockerfile | 2 –  
 lde\_config/ldc/php-fpm/system-config.ini | 122 ——————————-  
 lde\_config/lde/system-config.ini | 117 —————————–  
 9 files changed, 243 insertions(+), 243 deletions(-)  
 create mode 100644 config/system-config.ldc.ini  
 create mode 100644 config/system-config.lde.ini  
 delete mode 100644 lde\_config/ldc/php-fpm/system-config.ini  
 delete mode 100644 lde\_config/lde/system-config.ini  
bisect found first bad commit%  
  
Ok, now we know where the file has gone! (bearbeitet)   
  
  
  
Options  
git log –stat –full-history — lde\_config/ldc/php-fpm/system-config.ini  
  
that’s the bit that confuses me. It looks like full-history limits the history pruning it does. I suspect there might be something like sorting by date rather than commit order at play.  
 vor 4 Minuten  
It include a number of seemingly unrelated merges  
 vor 3 Minuten  
with –stat, you can see the addition, change, and ultimate deletion  
  
  
https://git-scm.com/docs/git-log#Documentation/git-log.txt—grep-reflogltpatterngtWhat if you will add  
  
-g  
–walk-reflogs   
  
You’d need –walk-reflog, but I think this would only work on your local reflog, so not when someone else deleted the file, and you just pulled the changes in.  
  
for github you have access to repository reflog  
https://objectpartners.com/2014/02/11/recovering-a-commit-from-githubs-reflog/ </andrew.morrison>@learnosity.com&gt; </andrew.morrison>