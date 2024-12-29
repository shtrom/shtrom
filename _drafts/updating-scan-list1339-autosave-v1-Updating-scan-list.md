---
id: 1445
title: 'Updating scan list'
date: '2024-03-11T18:22:04+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1445'
permalink: '/?p=1445'
footnotes:
    - ''
---

- I want to close my [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/) with some progress
- Haven’t worked out the CTCSS module or frequency encoding yet
- I can change the scan list to local repeaters 
    - Got the [updated repeater list from the WIA](https://www.wia.org.au/members/repeaters/data/)
    - Played with VLOOKUP in LibreOffice 
        - Also, conditional formatting, but [had to file a bug](https://bugs.documentfoundation.org/show_bug.cgi?id=159396)
- Also copying the 2m FM call freq to channel 0
- With minipro, now that it supports the T48
- It helps to flash the updated code, rather than the original and get confused that nothing changed
- Manually changing [ihex](https://en.wikipedia.org/wiki/Intel_HEX) means having to recalculate the checksum for the modified lines 
    - This helps [https://www.fischl.de/hex\_checksum\_calculator/?](https://www.fischl.de/hex_checksum_calculator/?)
- ….and it worked!
- Next on the list: 
    - Setting the CTCSS to a more practical tone for the local repeaters
    - Making some sort of controllable CTCSS circuit compatible with the original, so it can be driven by the EPROM
    - Work out how the frequencies are encoded.

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-91 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbf635291"}" data-wp-interactive="core/image">![Screen shot of vim in diff mode, showing the difference between two files in IHEX format](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/image-5.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screen shot of vim in diff mode, showing the difference between two files in IHEX format" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbf6357ab"}" data-wp-interactive="core/image">![Screenshot of a terminal running minipro to flash a 28C16 EPROM with a Xgecu T48 programmer](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-27-23-22-23.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screenshot of a terminal running minipro to flash a 28C16 EPROM with a Xgecu T48 programmer" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>