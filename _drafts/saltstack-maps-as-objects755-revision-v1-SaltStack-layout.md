---
id: 972
title: 'SaltStack layout'
date: '2023-08-07T00:15:49+10:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=972'
permalink: '/?p=972'
---

I use [SaltStack](http://saltstack.com) to manage my systems’ configurations. This allows me to have a relatively structured way to maintain them, and set up new ones. There are, however, many ways to set up SaltStack states. I have honed my favourite approach by trial-and-error, which I want to touch on here. It’s nothing too esoteric, but worth a summary for clarity’s sake.

tl;dr:

- 

SaltStack has two main parts: the [*states*, which describe what needs to be done](https://docs.saltproject.io/salt/user-guide/en/latest/topics/states.html) (e.g., a file needs to be present with the desired content), and the [*pillar* which provide parameters for the states](https://docs.saltproject.io/salt/user-guide/en/latest/topics/pillar.html) (e.g., the name of the file, and/or its content). Both are key-value objects, and the pillar is generally the place where sensitive information such as passwords can be stored.

XXX: init + includes

They are generally written in YAML, and often [extended using Jinja](https://docs.saltproject.io/salt/user-guide/en/latest/topics/jinja.html). With the use of Jinja, it is also possible to define [maps of static values and other varying sets of options](https://docs.saltproject.io/salt/user-guide/en/latest/topics/map-files.html) (e.g., support for different OS’s paths).

The key to the way I set states up is that they generally rely on a parameter dictionary from the `map.jinja` file. The dictionary itself is built with default static values, overridable by the pillar. The structure of the dictionary is very templated, with common variable names (e.g., `server_pkg`, `git_url`, `database_name`, `app_username`, …) reused across states. This allows me to use the maps as little objects that can be imported by other states.

```
{% set <+APP+> = salt['grains.filter_by'](                                                                                                                              
{ 
  'ArchLinux': { ... },
  'OpenBSD': { ... },                                                                                                                                                                   
  'default': {                                                                                                                                                          
    'pkg': '<+APP+>',                                                                                                                                                   
    'server_pkg': '<+APP+>-server',                                                                                                                                     
    'client_pkg': '<+APP+>-client',                                                                                                                                     
                                                                                                                                                                        
    'service': '<+APP+>',                                                                                                                                               
                                                                                                                                                                        
    'git_url': '',                                                                                                                                                      
    'git_branch': 'master',                                                                                                                                             
                                                                                                                                                              
    'user': '<+APP+>',                                                                                                                                                  
                                                                                                                                                    
    'install_path': '/opt/<+APP+>',                                                                                                                                     
    'datadir': '/srv/<+APP+>',            

    'web_path': '/<+APP+>',               
    'base_url': 'https://' + domain,        

    'host': 'localhost',
    'port': <+PORT+>,

    # app-specific config
    'api_key': '',
    'http_username': '',
    'http_password_hash': '',
    },
  },
  merge=salt['pillar.get']('<+APP+>')
)
%}
```

This is particularly useful for two reasons. First, common actions (e.g., user creation, service instalation, …) can be done via Jinja macros. This avoids repeating boilerplate code, and offers faster update paths when I need to change how particular actions get done.

<figure class="wp-block-image size-full">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/08/image-4.png)</figure>This also allows other states to reuse the information fairly transparently. One such case is when building web server configuration: proxy configuration for multiple web apps can be generated automatically pointing `web_path` to `host`:`port`.

<figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/08/image-1024x315.png)</figure>  
 you have SLS files that define states.If you have a bunch of variables that configure a state for say, on OS, or a region, or something like that, such as paths or versions, this generally goes to the map.jinja. You can import it from the state, and use the Jinja variables when defining your state (yes, your SLS file is a Jinja file. Don’t abuse it. Great power. Great responsibility yadda yadda).Now, if you want to generate a configuration file, you can also use a Jinja template. The SLS file will have a file.managed: { “template”: “jinja”, “context”: {…}, …}. The context should contain all the variables that you want the Jinja config template to use.  
  
Another advantage of map.jinja files is that other packages can import them in their own state. In this example, you could use the host, port and webpath, to also create an nginx.conf that proxies it nicely.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-24 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt1-1024x70.png)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt2-697x1024.png)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt4.png)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/01/salt5-1024x467.png)</figure></figure>