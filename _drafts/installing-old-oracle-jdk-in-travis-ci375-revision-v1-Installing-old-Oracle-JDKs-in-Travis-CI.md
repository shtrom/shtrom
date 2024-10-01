---
id: 686
title: 'Installing old Oracle JDKs in Travis-CI'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=686'
permalink: '/?p=686'
---

We’ve [been here before](https://blog.narf.ssji.net/2016/05/download-oracle-jdk-without-nagscreens/), but Oracle keeps being a pain in everyone’s rear end. This time, we want to keep testing against version 7 of the JDK with Travis CI.

Oracle has [stopped supporting version 7 of the JDK](http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html). This just means they added more hoops for you to get to it and do your job.

This in turns has [broken other good people’s packaging efforts](http://www.webupd8.org/2017/06/why-oracle-java-7-and-6-installers-no.html), which led [Travis CI to no longer support old JDKs](https://github.com/travis-ci/travis-ci/issues/7964#issuecomment-316771821).

The problem is that, while no longer supported, the Oracle JDK 7 is still in use. If you want to keep having visibility about how well your tools work with it, automated testing is the sanest way to do it. So you need to get that JDK onto your Travis CI instance in some way.

Fortunately, there are [some convenient mirrors still providing access to the binaries](https://stackoverflow.com/a/44151028) (namely, [OSUOSL](http://ftp.osuosl.org/pub/funtoo/distfiles/oracle-java/)) . So let’s use those.

Here’s a minimum .travis.yml fixing this issue.

```
language: java
jdk:
  - oraclejdk7

before_install:
  - if [ "${TRAVIS_JDK_VERSION}" == "oraclejdk7" ]; then export JAVA_HOME="/usr/lib/jvm/java-7-oracle"; export PATH="${JAVA_HOME}/bin:${PATH}"; fi
  - test "${TRAVIS_JDK_VERSION}" != "oraclejdk7" || (test ! -d "${JAVA_HOME}" && (curl http://ftp.osuosl.org/pub/funtoo/distfiles/oracle-java/jdk-7u80-linux-x64.tar.gz | sudo tar xz -C /usr/lib/jvm; sudo mv /usr/lib/jvm/jdk1.7.0_80 "${JAVA_HOME}"))

script:
  - java -version
```

Thanks Oracle… NOT.