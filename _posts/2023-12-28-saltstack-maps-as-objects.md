---
id: 755
title: 'SaltStack maps as objects'
date: '2023-12-28T00:06:16+11:00'
author: 'Olivier Mehani'
excerpt: 'My favourite approach to writing SaltStack states for configuration management revolves around map.jinja following a templated pattern. This helps for decoupling of the parameters and reuse/sharing in multiple states.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=755'
permalink: /2023/12/28/saltstack-maps-as-objects/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '14'
image: /wp-content/uploads/sites/3/2023/08/image-4.png
categories:
    - code
    - engineering
    - sysadmin
    - tip
tags:
    - SaltStack
---

I use [SaltStack](http://saltstack.com) to manage my systems’ configurations. This allows me to have a relatively structured way to maintain them, and set up new ones. There are, however, many ways to set up SaltStack states. I have honed my favourite approach by trial-and-error, which I want to touch on here. It’s nothing too esoteric, but worth a summary for clarity’s sake.

tl;dr:

- States in SLS files should have as few parameter strings as possible.
- Parameters should instead come from `map.jinja` files.
- Maps should generally allow an override by similarly-named pillar keys.
- Map dicts should be as formulaic as possible, similar to OOP objects implementing interfaces.

This last point is the key, as it makes it easy to

- leverage existing maps without having to work out the specific details of each one,
- use macros for common tasks (directory creation, user setup, package and service management, …), and
- share maps across states (e.g., making web applications’ URIs accessible via a web server)

SaltStack has two main parts: the [*states*, which describe what needs to be done](https://docs.saltproject.io/salt/user-guide/en/latest/topics/states.html) (e.g., a file needs to be present with the desired content), and the [*pillar* which provides parameters for the states](https://docs.saltproject.io/salt/user-guide/en/latest/topics/pillar.html) (e.g., the name of the file, and/or its content). Both are key-value objects, and the pillar is generally the place where [sensitive information such as passwords can be stored, encrypted](https://docs.saltproject.io/en/latest/topics/pillar/index.html#pillar-encryption). They are generally written in YAML, and often [extended using Jinja](https://docs.saltproject.io/salt/user-guide/en/latest/topics/jinja.html).

With the use of Jinja, it is also possible to define [maps of static values and other varying sets of options](https://docs.saltproject.io/salt/user-guide/en/latest/topics/map-files.html) (e.g., support for different OS’s paths below, lines 3–5).

{% raw %}
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
    'base_url': 'https://<+DOMAIN+>',        

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
{% endraw %}

The key to the way I set states up is that they generally rely on a parameter dictionary from the `map.jinja` file. The dictionary itself is built with default static values, overridable by the pillar (line 32).

The structure of the dictionary is very templated, with common variable names (e.g., `server_pkg`, `git_url`, `database_name`, `app_username`, …) reused across states. This allows me to use the maps as little objects that can be imported by other states.

This is particularly useful for two reasons. First, common actions (e.g., user creation, service installation, …) can be done via Jinja macros. This avoids repeating boilerplate code, and offers faster update paths when I need to change how particular actions get done.

<figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2023\/08\/image-4.png","figureClassNames":"wp-block-image size-full","figureStyles":null,"imgClassNames":"wp-image-970","imgStyles":null,"targetWidth":943,"targetHeight":309,"scaleAttr":false,"ariaLabel":"Enlarge image: Screenshot of Vim editing SaltStack files for a Nextcloud state: map.jinja, a state file using macros to setup user and groups, and a Jinja macro processing the map data to do so.","alt":"Screenshot of Vim editing SaltStack files for a Nextcloud state: map.jinja, a state file using macros to setup user and groups, and a Jinja macro processing the map data to do so."}" data-wp-interactive="core/image">![Screenshot of Vim editing SaltStack files for a Nextcloud state: map.jinja, a state file using macros to setup user and groups, and a Jinja macro processing the map data to do so.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/08/image-4.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screenshot of Vim editing SaltStack files for a Nextcloud state: map.jinja, a state file using macros to setup user and groups, and a Jinja macro processing the map data to do so." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button><figcaption class="wp-element-caption">Screenshot of Vim editing SaltStack files for a Nextcloud state: map.jinja, a state file using macros to setup user and groups, and a Jinja macro processing the map data to do so.</figcaption></figure>This also allows other states to reuse the information fairly transparently. One such case is when building web server configuration: proxy configuration for multiple web apps can be generated automatically pointing `web_path` to `host`:`port`. With such a setup, adding a new application to an nginx virtualhost is nothing more than `import`ing the application’s map, and adding it to the list used to generate the `locations`.

<figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2023\/08\/image.png","figureClassNames":"wp-block-image size-full","figureStyles":null,"imgClassNames":"wp-image-965","imgStyles":null,"targetWidth":1336,"targetHeight":411,"scaleAttr":false,"ariaLabel":"Enlarge image: Screenshot of Vim editing SaltStack files for an Nginx state: a state file importing a number of different maps and putting them in context to render the configuration file, and the Jinja template for the configuration file, iterating over the applications in context.","alt":"Screenshot of Vim editing SaltStack files for an Nginx state: a state file importing a number of different maps and putting them in context to render the configuration file, and the Jinja template for the configuration file, iterating over the applications in context."}" data-wp-interactive="core/image">![Screenshot of Vim editing SaltStack files for an Nginx state: a state file importing a number of different maps and putting them in context to render the configuration file, and the Jinja template for the configuration file, iterating over the applications in context.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/08/image.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screenshot of Vim editing SaltStack files for an Nginx state: a state file importing a number of different maps and putting them in context to render the configuration file, and the Jinja template for the configuration file, iterating over the applications in context." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button><figcaption class="wp-element-caption">Screenshot of Vim editing SaltStack files for an Nginx state: a state file importing a number of different maps and putting them in context to render the configuration file, and the Jinja template for the configuration file, iterating over the applications in context.</figcaption></figure>As noted earlier all of the parameters can be overridden from the pillar. The map takes care of fetching and merging this data, which means that none of the states using the map need to have any direct knowledge about the pillar structure.

In short, using `map.jinja` to generate dicts that follow a templated pattern allows to neatly group all the parameters describing an application into a single source-of-truth object. This also decouples all the states from the source of the parameters, and the regular pattern of the maps makes it easy to share and reuse the information in multiple states, or quickly add support for new applications.
