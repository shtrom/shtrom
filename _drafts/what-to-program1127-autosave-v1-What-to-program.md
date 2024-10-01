---
id: 1460
title: 'What to program?'
date: '2024-03-11T18:36:55+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1460'
permalink: '/?p=1460'
footnotes:
    - ''
---

On [updating channel memory on decommissioned AWA RT85 radio](https://blog.narf.ssji.net/2023/11/25/updating-channel-memory-awa-rt85-ham-radio/): now that I have done the [EPROM switcharoo](https://blog.narf.ssji.net/2023/12/31/eprom-switcharoo/), and got a dump of the memory, I need to understand what to write into it.

- Found a [dump of RT85-related info](http://www.unixsupport.com.au/hamradio/radios/awa/rt85/), including a [copy of Brad VK3TAE’s page](http://www.unixsupport.com.au/hamradio/radios/awa/rt85/rt85mods2.html)
    - but not the [programming guide](https://web.archive.org/web/20050615023352/http://keycom.d2.net.au/rt85.pdf), which is the most useful to continue
- Made a spreadsheet of what I know the radio is programmed with, and matching to what’s in the EPROM 
    - Some personality settings at `0x3f0`–`0x3f3`
        - not sure what `0x3f4` set to `0x51` means 
            - it could very well be due to a misunderstanding of the [official programming manual](http://www.unixsupport.com.au/hamradio/radios/awa/rt85/rt85%20manual.pdf) (page F.1-8)
    - 59 Channels programmed (`0x3f0` set to `0x59`) 
        - RX from `0x0` to `0x18f`; TX from `0x400` to `0x58f`
        - Channels are grouped in 10s, at `0x0`, `0x40` , `0xc0`, `0x100` and `0x140`
        - Channel 0 seems to be at `0x164`, which would be channel 60
        - Channel spacing is 5kHz (CTCSS disabled code is either `0x00` or `0x40`) 
            - The available CTCSS list is not a complete overlap with those in use in the [ACMA repeater list](https://www.wia.org.au/members/repeaters/data/documents/Repeater%20Directory%20231229.pdf); most notably missing is 91.5Hz
        - Programmed for the 150 `VHF(HB)` band (`0x404`, `0x40c`, `0x410` set to `0x72`, `0x56`, `0x02`)
- Not sure how the frequency programming actually works: how to map the remaining 2 bytes to the desired frequency? 
    - Threw a call out on the Fediverse for more info [https://piaille.fr/@shtrom/111678916122686083](<https://piaille.fr/@shtrom/111678916122686083 >)

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-105 is-layout-flex wp-block-gallery-is-layout-flex"></figure><div class="wp-block-jetpack-tiled-gallery aligncenter is-style-rectangular"><div class="tiled-gallery__gallery"><div class="tiled-gallery__row"><div class="tiled-gallery__col" style="flex-basis:45.86143%"><figure class="tiled-gallery__item">[![A spreadsheet open in LibreOffice, mapping the contents of the EPROM, and its understood meaning so far.](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-01-17-55-59-1024x576.png?ssl=1)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-01-17-55-59-1024x576.png)</figure></div><div class="tiled-gallery__col" style="flex-basis:54.13857%"><figure class="tiled-gallery__item">[![Excerpt from the RT85 Programming Manual, with an example of how to program 0x51 at address 0x3F3](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-01-18-56-38.png?ssl=1)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-01-18-56-38.png)</figure></div></div></div></div>