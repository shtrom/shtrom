---
id: 1265
title: 'The burninator'
date: '2024-01-21T22:48:38+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1265'
permalink: /2024/01/21/the-burninator/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
iawp_total_views:
    - '2'
image: /wp-content/uploads/sites/3/2024/01/PXL_20240121_113318359-copy.jpg
categories:
    - electronics
    - µblog
tags:
    - 'water tank sensor'
format: status
---

- Looked at the ESP32-POE’s schematic [https://github.com/OLIMEX/ESP32-POE/blob/master/HARDWARE/ESP32-PoE-hardware-revision-K/ESP32-PoE\_Rev\_K.pdf ](<https://github.com/OLIMEX/ESP32-POE/blob/master/HARDWARE/ESP32-PoE-hardware-revision-K/ESP32-PoE_Rev_K.pdf >)
    - Found a nice 46V from the Ethernet connector to power the [4–20mA Current Loop Rain Water Tank Sensor](https://blog.narf.ssji.net/2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/)
    - Tapped that
- Replaced the resistor with a 100Ω 
    - Burnt the resistor…
- Put the 270Ω back in 
    - Also burnt it
- Turns out the sensor doesn’t want “anything up to 48V” as I thought, but just 24V 
    - The 12V from the Arduino seemed ok, so I got complacent
    - No sign of a 24V line
    - Need to create one with a regulator

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-10 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2024\/01\/signal-2024-01-21-222150_002.jpeg","figureClassNames":"wp-block-image size-large","figureStyles":null,"imgClassNames":"wp-image-1266","imgStyles":null,"targetWidth":1080,"targetHeight":1028,"scaleAttr":false,"ariaLabel":"Enlarge image: Setup diagram for a 4-20mA pressure sensor, translated by Google Lens.","alt":"Setup diagram for a 4-20mA pressure sensor, translated by Google Lens."}" data-wp-interactive="core/image">![Setup diagram for a 4-20mA pressure sensor, translated by Google Lens.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/signal-2024-01-21-222150_002-1024x975.jpeg)<button aria-haspopup="dialog" aria-label="Enlarge image: Setup diagram for a 4-20mA pressure sensor, translated by Google Lens." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2024\/01\/PXL_20240121_113318359-copy.jpg","figureClassNames":"wp-block-image size-large","figureStyles":null,"imgClassNames":"wp-image-1267","imgStyles":null,"targetWidth":2048,"targetHeight":1536,"scaleAttr":false,"ariaLabel":"Enlarge image: The adapter connecting the sensor to the ESP32, with a very charred resistor.","alt":"The adapter connecting the sensor to the ESP32, with a very charred resistor."}" data-wp-interactive="core/image">![The adapter connecting the sensor to the ESP32, with a very charred resistor.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/PXL_20240121_113318359-copy-1024x768.jpg)<button aria-haspopup="dialog" aria-label="Enlarge image: The adapter connecting the sensor to the ESP32, with a very charred resistor." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>