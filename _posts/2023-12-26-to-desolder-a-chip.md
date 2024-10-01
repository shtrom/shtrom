---
id: 1092
title: 'To desolder a chip'
date: '2023-12-26T20:33:19+11:00'
author: 'Olivier Mehani'
excerpt: 'Back onto the RT85 programming, I tried to desolder the 27C16 EPROM. Solder wick didn''t work. Next step: el-cheapo hot air gun.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1092'
permalink: /2023/12/26/to-desolder-a-chip/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
image: /wp-content/uploads/sites/3/2023/12/PXL_20231226_084730625-scaled.jpg
categories:
    - electronics
    - ham
    - µblog
tags:
    - 'AWA RT85'
format: status
---

Back onto the [RT85 programming](https://blog.narf.ssji.net/2023/11/25/updating-channel-memory-awa-rt85-ham-radio/), I tried to desolder the 27C16 EPROM from the Z-273 module that carries it. I went down the path of the solder wick, but didn’t have much success making the chip move despite a lot of solder being removed.

Being as equipped as I usually am, akin to from a second-hand budget store, I don’t have a hot air rework station. According to [this video](https://www.youtube.com/watch?app=desktop&v=fb7iWSXNta4), I may be able to get away with an el-cheapo all-purpose hot air gun from Bunnings, and a beer tin to fashion a nozzle out of. I’ll give that a go.

On unrelated matters, does anyone have the personality details of a RT85A data reprogrammed to the 2m Ham bands? Asking for a friend who might need it very soon.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-4 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2023\/12\/PXL_20231226_084730625-scaled.jpg","figureClassNames":"wp-block-image size-large","figureStyles":null,"imgClassNames":"wp-image-1095","imgStyles":null,"targetWidth":1920,"targetHeight":2560,"scaleAttr":false,"ariaLabel":"Enlarge image: The backside of the Z-273 module, showing mostly desoldered EPROM pads.","alt":"The backside of the Z-273 module, showing mostly desoldered EPROM pads."}" data-wp-interactive="core/image">![The backside of the Z-273 module, showing mostly desoldered EPROM pads.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/12/PXL_20231226_084730625-768x1024.jpg)<button aria-haspopup="dialog" aria-label="Enlarge image: The backside of the Z-273 module, showing mostly desoldered EPROM pads." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large is-style-default wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2023\/12\/PXL_20231226_081222795-scaled.jpg","figureClassNames":"wp-block-image size-large is-style-default","figureStyles":null,"imgClassNames":"wp-image-1096","imgStyles":null,"targetWidth":1920,"targetHeight":2560,"scaleAttr":false,"ariaLabel":"Enlarge image: The Z-273 module from an RT85A radio, with an EPROM in place.","alt":"The Z-273 module from an RT85A radio, with an EPROM in place."}" data-wp-interactive="core/image">![The Z-273 module from an RT85A radio, with an EPROM in place.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/12/PXL_20231226_081222795-768x1024.jpg)<button aria-haspopup="dialog" aria-label="Enlarge image: The Z-273 module from an RT85A radio, with an EPROM in place." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>