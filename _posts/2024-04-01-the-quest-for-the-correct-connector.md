---
id: 1477
title: 'The quest for the correct connector'
date: '2024-04-01T00:22:46+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1477'
permalink: /2024/04/01/the-quest-for-the-correct-connector/
activitypub_status:
    - federated
image: /wp-content/uploads/sites/3/2024/03/Screenshot-from-2024-03-31-23-44-50.png
categories:
    - µblog
tags:
    - 'AWA RT85'
format: status
---

- Need to find a connector that actually connects to the [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/). 
    - M20 headers with a 2.54mm pitch fit, but I don’t get contact
- Asked for help on Mastodon <https://piaille.fr/@shtrom/112068949230147198>
    - JST was mentionned… But which one? Maybe EH? <https://www.mattmillman.com/info/crimpconnectors/common-jst-connector-types/#eh >
    - Mouser has EH08 connectors <https://au.mouser.com/ProductDetail/ADI-Trinamic/CABLE-EH08?qs=QNEnbhJQKvYBGV1Xer3yZA%3D%3D>
- Reviewed the RT85 doc 
    - I need connectors for J358 (audio in/out), <s>and J901 (CTCSS programming data)</s> [no, see next post](https://blog.narf.ssji.net/2024/04/01/the-quest-for-the-correct-connector-contd/)
    - J358 is an EMCS0852M 
        - Found an [EMCS-0352M on eBay](https://www.ebay.com.au/itm/112209764280), which looks the same: “EMCS-0352M SUMIKO TEC CONNECTOR 3 POSITION” 
            - No 8-position on eBay, though
            - Can’t find the datasheet to confirm size
    - <s>J901 is an PS-11SD-S4TS1-1; Mouser only has 15SD, though: [https://au.mouser.com/datasheet/2/206/JAEIS05057\_1-2550519.pdf](https://au.mouser.com/datasheet/2/206/JAEIS05057_1-2550519.pdf), but they are 2.54mm pitch headers</s> [not relevant](https://blog.narf.ssji.net/2024/04/01/the-quest-for-the-correct-connector-contd/)

<figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd79fd4"}" data-wp-interactive="core/image">![The description below refers to the circuit diagram which follows this section. The Z-281 Encoder/Decoder is an optionally fitted printed circuit board that mounts on the underside of the transceiver, and plugs directly into connector J 358 on the Receiver PCB and J901 on the EPROM module.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/Screenshot-from-2024-03-31-23-43-01.png)<button aria-haspopup="dialog" aria-label="Enlarge image: The description below refers to the circuit diagram which follows this section. The Z-281 Encoder/Decoder is an optionally fitted printed circuit board that mounts on the underside of the transceiver, and plugs directly into connector J 358 on the Receiver PCB and J901 on the EPROM module." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-15 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd7a668"}" data-wp-interactive="core/image">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/Screenshot-from-2024-03-31-23-43-34.png)<button aria-haspopup="dialog" aria-label="Enlarge image" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"imageId":"6770cbdd7ab46"}" data-wp-interactive="core/image">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/Screenshot-from-2024-03-31-23-44-50.png)<button aria-haspopup="dialog" aria-label="Enlarge image" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>