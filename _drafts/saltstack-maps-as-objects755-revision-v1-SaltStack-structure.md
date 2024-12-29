---
id: 763
title: 'SaltStack structure'
date: '2023-01-06T10:38:15+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=763'
permalink: '/?p=763'
---

map.jinja Ideally, we should explicitely pass all wanted variables (as the context) to the template, but we often just reach into the pillar straight from the template. This makes them generally a lot more complex than they need to be.  
  
 you have SLS files that define states.If you have a bunch of variables that configure a state for say, on OS, or a region, or something like that, such as paths or versions, this generally goes to the map.jinja. You can import it from the state, and use the Jinja variables when defining your state (yes, your SLS file is a Jinja file. Don’t abuse it. Great power. Great responsibility yadda yadda).Now, if you want to generate a configuration file, you can also use a Jinja template. The SLS file will have a file.managed: { “template”: “jinja”, “context”: {…}, …}. The context should contain all the variables that you want the Jinja config template to use.  
  
Another advantage of map.jinja files is that other packages can import them in their own state. In this example, you could use the host, port and webpath, to also create an nginx.conf that proxies it nicely.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-20 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt1-1024x70.png)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt2-697x1024.png)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt3-950x1024.png)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt4.png)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt5-1024x467.png)</figure></figure>