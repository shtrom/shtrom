---
id: 671
title: 'GitHub Pull Request: mark all files as viewed'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
excerpt: 'Here goes a one-liner for the JS console to mark all files as viewed at once in a Github PR.'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=671'
permalink: '/?p=671'
---

GitHub now allows to [expand/collapse all files in a PR diff at once](https://github.com/refined-github/refined-github/issues/2151 "https://github.com/refined-github/refined-github/issues/2151") (pressing `Alt` while clicking one of the toggles). Unfortunately, there is no similar feature to mark all files as viewed. This is handy after having reviewed meaningful changes to file, and automatically modified/generated files can be ignored.

So here goes a one-liner for the JS console.

```
Array.from(document.getElementsByClassName('js-reviewed-toggle')).forEach(c => c.getElementsByTagName('input')[0].checked || c.click())
```

<figure class="wp-block-image size-full">[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/11/Screen-Shot-2021-11-16-at-13.53.56.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/11/Screen-Shot-2021-11-16-at-13.53.56.jpg)</figure>