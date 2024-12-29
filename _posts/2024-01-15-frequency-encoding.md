---
id: 1234
title: 'Frequency encoding'
date: '2024-01-15T00:23:22+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1234'
permalink: /2024/01/15/frequency-encoding/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
image: /wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-13-23-55-35.png
categories:
    - electronics
    - ham
    - hardware
    - µblog
tags:
    - 'AWA RT85'
format: status
---

- [Pages B.1-3 to B.1-7 of the RT-85 handbook ](http://www.unixsupport.com.au/hamradio/radios/awa/rt85/rt85%20manual.pdf#page=25)have information about how the frequency is generated from the information in the EPROM 
    - Covers UHF, VHF(LB) and VHF(HB). The 2m band is VHF(HB) (148–174)
    - Xtal @5.12Mhz
    - *f<sub>ref</sub>* = 5 kHz channels
    - *M* = 63
    - *f<sub>out</sub>* = ( *a* (*M*+1 )+ *M* (*n*–*a*) )*f<sub>ref</sub>*
        - *n* is the 10 LSbs of the 3-byte frequency code
        - *a* is the next 7 LSbs
    - *f<sub>out</sub>* then get mixed some more
    - *f<sub>0</sub>* = *f<sub>L</sub>* + *N<sub>2</sub>*/*N<sub>1</sub>* \* *f<sub>s</sub>*
        - *f<sub>L</sub>* may by the same as *f<sub>out</sub>*
        - *N<sub>1</sub>* = 4
        - *N<sub>2</sub>* = 16
    - not everything lines up yet
- Got my half taken-apart [BF-F9 to scan for a receive tone](https://www.youtube.com/watch?v=lBFFDHyZeww) and confirmed that the CTCSS module outputs a 91.5Hz tone (and that both TX and RX work)

<figure class="wp-block-gallery has-nested-images columns-default wp-block-gallery-8 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd4e3d4"}" data-wp-interactive="core/image">![Page B.1-5 of the RT 85 manual, showing the main frequency synthetiser.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-13-23-55-35.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Page B.1-5 of the RT 85 manual, showing the main frequency synthetiser." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd4e9c2"}" data-wp-interactive="core/image">![Page B.1-3 of the RT 85 manual, describing how the EPROM data is used to configure the main frequency synthetiser](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/image.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Page B.1-3 of the RT 85 manual, describing how the EPROM data is used to configure the main frequency synthetiser" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd4eff5"}" data-wp-interactive="core/image">![Page B.1-7 of the RT 85 manual, showing the transmit PLL](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-13-23-59-48.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Page B.1-7 of the RT 85 manual, showing the transmit PLL" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd4f5e7"}" data-wp-interactive="core/image">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/PXL_20240114_060856246.MP-copy-1024x768.jpg)<button aria-haspopup="dialog" aria-label="Enlarge image" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>