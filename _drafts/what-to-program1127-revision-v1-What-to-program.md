---
id: 1461
title: 'What to program?'
date: '2024-03-11T18:37:43+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1461'
permalink: '/?p=1461'
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

<figure class="wp-block-gallery has-nested-images columns-default wp-block-gallery-107 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbf66f8ba"}" data-wp-interactive="core/image">![A spreadsheet open in LibreOffice, mapping the contents of the EPROM, and its understood meaning so far.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-01-17-55-59-1024x576.png)<button aria-haspopup="dialog" aria-label="Enlarge image: A spreadsheet open in LibreOffice, mapping the contents of the EPROM, and its understood meaning so far." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbf66fe1d"}" data-wp-interactive="core/image">![Excerpt from the RT85 Programming Manual, with an example of how to program 0x51 at address 0x3F3](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-01-18-56-38.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Excerpt from the RT85 Programming Manual, with an example of how to program 0x51 at address 0x3F3" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>