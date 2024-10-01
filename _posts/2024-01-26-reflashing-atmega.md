---
id: 1322
title: 'Reflashing ATMEGA'
date: '2024-01-26T17:39:53+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1322'
permalink: /2024/01/26/reflashing-atmega/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
iawp_total_views:
    - '11'
image: /wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-47-14-1.png
categories:
    - electronics
    - hardware
    - µblog
tags:
    - Arduino
    - minipro
    - 'Xgecu T48'
format: status
---

- Maybe I didn’t [fry my ATMEGA328P](https://blog.narf.ssji.net/2023/12/16/to-kill-a-chip/), but just wiped it?
- <https://forum.arduino.cc/t/arduino-bootloader-for-atmega-128/131410/2>
- Bootloaders in `~/.arduino15/packages/arduino/hardware/avr/1.8.6/bootloaders/atmega``
- Can’t program the old one
- Can program the new one
- Still can’t program it in the dev board 
    - … So I also killed the dev board…
- … or it’s not the right bootloader? 
    - `ATmegaBOOT_168_atmega328.hex` didn’t work
    - `ATmegaBOOT_168_atmega328_pro_8MHz.hex` didn’t work
    - <https://forum.arduino.cc/t/bootloader-hex/562248/3> seems to indicate the bootloader for the 323P is not in there
    - available from [https://github.com/Optiboot/optiboot/blob/master/optiboot/bootloaders/optiboot/optiboot\_atmega328.hex](https://github.com/Optiboot/optiboot/blob/master/optiboot/bootloaders/optiboot/optiboot_atmega328.hex)
        - … still didn’t work…
- Note to self, `minipro` has merged initial support for the T48 pogrammer: <https://gitlab.com/DavidGriffith/minipro/-/commit/db11c39ec03c0bf7d67cf63c8ededc0be17f1eec>
    - `./minipro -p AT28C16@DIP24 -r - -f ihex master`
        - it works well! [https://gitlab.com/DavidGriffith/minipro/-/issues/294#note\_1744336371](https://gitlab.com/DavidGriffith/minipro/-/issues/294#note_1744336371)

<figure class="wp-block-gallery has-nested-images columns-1 is-cropped wp-block-gallery-12 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2024\/01\/Screenshot-from-2024-01-26-16-46-51-1.png","figureClassNames":"wp-block-image size-full","figureStyles":null,"imgClassNames":"wp-image-1327","imgStyles":null,"targetWidth":687,"targetHeight":431,"scaleAttr":false,"ariaLabel":"Enlarge image: Screenshot of Xgpro having failed to reprogram a fried ATMEGA328p","alt":"Screenshot of Xgpro having failed to reprogram a fried ATMEGA328p"}" data-wp-interactive="core/image">![Screenshot of Xgpro having failed to reprogram a fried ATMEGA328p](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-46-51-1.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screenshot of Xgpro having failed to reprogram a fried ATMEGA328p" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2024\/01\/Screenshot-from-2024-01-26-16-47-14-1.png","figureClassNames":"wp-block-image size-full","figureStyles":null,"imgClassNames":"wp-image-1326","imgStyles":null,"targetWidth":1015,"targetHeight":497,"scaleAttr":false,"ariaLabel":"Enlarge image: Screenshot of Xgpro having successfully programmed an ATMEGA328p","alt":"Screenshot of Xgpro having successfully programmed an ATMEGA328p"}" data-wp-interactive="core/image">![Screenshot of Xgpro having successfully programmed an ATMEGA328p](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-47-14-1.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screenshot of Xgpro having successfully programmed an ATMEGA328p" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>