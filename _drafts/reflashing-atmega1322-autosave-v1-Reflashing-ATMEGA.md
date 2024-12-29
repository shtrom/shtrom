---
id: 1449
title: 'Reflashing ATMEGA'
date: '2024-03-11T18:26:09+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1449'
permalink: '/?p=1449'
footnotes:
    - ''
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

<figure class="wp-block-gallery has-nested-images columns-1 is-cropped wp-block-gallery-95 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-full">![Screenshot of Xgpro having failed to reprogram a fried ATMEGA328p](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-46-51-1.png)</figure><figure class="wp-block-image size-full">![Screenshot of Xgpro having successfully programmed an ATMEGA328p](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-47-14-1.png)</figure></figure><div class="wp-block-jetpack-tiled-gallery aligncenter is-style-rectangular"><div class="tiled-gallery__gallery"><div class="tiled-gallery__row"><div class="tiled-gallery__col" style="flex-basis:43.86290%"><figure class="tiled-gallery__item">[![Screenshot of Xgpro having failed to reprogram a fried ATMEGA328p](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-46-51-1.png?ssl=1)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-46-51-1.png)</figure></div><div class="tiled-gallery__col" style="flex-basis:56.13710%"><figure class="tiled-gallery__item">[![Screenshot of Xgpro having successfully programmed an ATMEGA328p](https://i1.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-47-14-1.png?ssl=1)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-47-14-1.png)</figure></div></div></div></div>