---
id: 1022
title: '4&#8211;20mA Current Loop Rain Water Tank Sensor'
date: '2023-11-11T01:33:12+11:00'
author: 'Olivier Mehani'
excerpt: 'Our house water comes from a rain water tank. In dry weather, we need to get it topped up. While I enjoy tapping the side of the tank, I''d rather have a smoother system to know when to order a water delivery. The end goal is to have this reporting to HomeAssistant.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1022'
permalink: /2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
footnotes:
    - ''
image: /wp-content/uploads/sites/3/2023/11/PXL_20231009_132950832.jpg
categories:
    - µblog
tags:
    - HomeAssistant
    - 'water tank sensor'
---

Our house water comes from a rain water tank. In dry weather, we need to get it topped up. While I enjoy tapping the side of the tank, I’d rather have a smoother system to know when to order a water delivery. The end goal is to have this reporting to HomeAssistant. I have an Ethernet cable going to the water tank, and a PoE switch, so the plan is to control and power the whole monitoring system with one cable.

[µblog](https://blog.narf.ssji.net/category/%c2%b5blog/) tag: [water tank sensor](https://blog.narf.ssji.net/tag/water-tank-sensor/)

Progress so far:

- Dug up an old [Arduino Duemilanove](https://docs.arduino.cc/retired/boards/arduino-duemilanove) with an [ENC28J60 Ethernet Shield from eKitsZone](https://web.archive.org/web/20101231232442/http://www.ekitszone.com/)
    - I wanted to make it an IPv6 climate sensor for my beer-brewing shed 10 years ago, but got too busy with being distracted.
- Got a good-size [IP65 enclosure](https://www.jaycar.com.au/polycarbonate-enclosure-with-mounting-flange-171-w-x-121-d-x-55-h-mm/p/HB6219), and [cable glands](https://www.jaycar.com.au/10-14mm-dia-waterproof-cable-glands-pack-of-2/p/HP0736)
- Found documentation for both: 
    - [Duemilanove pinout](http://embdedsystems.blogspot.com/2013/11/arduino-duemilanove-pinout.html)
    - [ENC28J60 schematic](https://web.archive.org/web/20101122094127/http://www.ekitszone.com/download/enc28j60-schematic.pdf)
- Ordered a [4–20mA water pressure sensor from eBay](https://www.ebay.com.au/itm/284726104843)
- Dug up a PoE splitter
- Tested the sensor in a glass of water, it seems to work. 
    - Found an [example schematic of a 4–20mA setup with an Arduino](https://circuits4you.com/2016/05/13/arduino-4-20mamp-current-loop/)
    - The sensor can be powered directly from the `Vin` pin (6), which is the power from the barrel connector (from the PoE splitter), which is sufficient for the sensor
    - 250kΩ is not in the E12 resistors series, but 270kΩ is good enough
    - Nice in the [Arduino serial plotter](https://www.ebay.com.au/itm/284726104843)
    - Made a little daughter board for the sensor
- Found the [Ethercard library](https://www.arduino.cc/reference/en/libraries/ethercard/) to drive the Ethernet shield. 
    - The Duemilanove is not mentioned in the supported list, but the ATmega328 is an `avr`. It should work, right?
    - Hangs when configuring any sort of Ethernet parameter
- Need to debug 
    - First, look at the [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) ([Arduino doc](https://docs.arduino.cc/learn/communication/spi)), dug up my [BusPirate](http://dangerousprototypes.com/docs/Bus_Pirate_v3.5) ([SPI mode](http://dangerousprototypes.com/blog/bus-pirate-manual/bus-pirate-spi-guide/)).
    - Don’t have the right connectors, ordered [Bus Pirate v3 probe cable yellow labels](http://dirtypcbs.com/store/designer/details/ian/69/bus-pirate-v3-probe-cable-yellow-labels). Should have done that ages ago.
    - Note: Pin 13 on the Duemilanove is both `SCK` and the LED, so best not to try to fiddle with both at once

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-1 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231009_132806619.MP_-768x1024.jpg)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231009_132950832-1024x768.jpg)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231009_132954839-768x1024.jpg)</figure><figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231011_090443366-1024x768.jpg)</figure></figure><div class="wp-block-query is-layout-flow wp-block-query-is-layout-flow">- <div class="wp-block-columns is-layout-flex wp-container-core-columns-is-layout-1 wp-block-columns-is-layout-flex"><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:66.66%">### 4–20mA Current Loop Rain Water Tank Sensor
    
    </div><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:33.33%"><div class="has-text-align-right wp-block-post-date"><time datetime="2023-11-11T01:33:12+11:00">2023-11-11</time></div></div></div><div class="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow">Our house water comes from a rain water tank. In dry weather, we need to get it topped up. While I enjoy tapping the side of the tank, I’d rather have a smoother system to know when to order a water delivery. The end goal is to have this reporting to HomeAssistant. I have an Ethernet cable going to the water tank, and a PoE switch, so the plan is to control and power the whole monitoring system with one cable.
    
    [µblog](https://blog.narf.ssji.net/category/%c2%b5blog/) tag: [water tank sensor](https://blog.narf.ssji.net/tag/water-tank-sensor/)
    
     [<span aria-label="Continue reading 4–20mA Current Loop Rain Water Tank Sensor">(more…)</span>](https://blog.narf.ssji.net/2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/#more-1022)</div>
- <div class="wp-block-columns is-layout-flex wp-container-core-columns-is-layout-2 wp-block-columns-is-layout-flex"><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:66.66%">### To kill a chip
    
    </div><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:33.33%"><div class="has-text-align-right wp-block-post-date"><time datetime="2023-12-16T00:04:13+11:00">2023-12-16</time></div></div></div><div class="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow">
    - Received the handy header for the BusPirate
    - Wired everything, and somehow fried the ATMEGA328 
        - When programming from the Arduino IDE, it now complains as follow
    
    ```
    
    avrdude: stk500_recv(): programmer is not responding
    avrdude: stk500_getsync() attempt 1 of 10: not in sync: resp=0x00
    ...
    avrdude: stk500_recv(): programmer is not responding
    avrdude: stk500_getsync() attempt 10 of 10: not in sync: resp=0x00
    Problem uploading to board.  See https://support.arduino.cc/hc/en-us/sections/360003198300 for suggestions.
    ```
    
    
    - Trying reflash the microcontroller in the Xgegu T48 I got for [Updating channel memory on decommissioned AWA RT85 radio](https://blog.narf.ssji.net/2023/11/25/updating-channel-memory-awa-rt85-ham-radio/)
        - BFs BFs everywhere
    
    <figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-2 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">![Screenshot of Xgpro running in Wine](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/12/image-1024x576.png)<figcaption class="wp-element-caption">Using Xgpro in Wine with anXgecu T48 to test an ATMEGA328P. The chip seems dead…</figcaption></figure></figure>
    - Looks like I’m gonna have to get a new microcontroller… 
        - This is an opportunity to widen the search 
            - The ESP32-POE(-IND) could be a good fit <https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/open-source-hardware> <https://au.mouser.com/ProductDetail/Olimex-Ltd/ESP32-POE?qs=unwgFEO1A6tUQVMxdOBsBw%3D%3D >
                - Could save dev time by using <https://esphome.io/ > <https://mastodon.social/@flameeyes/111360625680537907>
    
    </div>
- <div class="wp-block-columns is-layout-flex wp-container-core-columns-is-layout-3 wp-block-columns-is-layout-flex"><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:66.66%">### Switching to ESP32
    
    </div><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:33.33%"><div class="has-text-align-right wp-block-post-date"><time datetime="2023-12-29T00:05:44+11:00">2023-12-29</time></div></div></div><div class="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow">
    - Order from Mouser arrived, with a replacement Atmega 328, and a selection of ESP32 boards
    - Duemilanove still fails to program with the same error as before on the new Atmega 
        - So I borked the dev board
        - But I might have two functional Atmega \\o/
    - Playing with the [ESP32-POE](https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/open-source-hardware)
        - I also ordered an -IND for the real deployment
        - Docs: <https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/resources/ESP32-POE-GPIO.png>, [https://github.com/OLIMEX/ESP32-POE/blob/master/HARDWARE/ESP32-PoE-hardware-revision-K/ESP32-PoE\_Rev\_K.pdf](https://github.com/OLIMEX/ESP32-POE/blob/master/HARDWARE/ESP32-PoE-hardware-revision-K/ESP32-PoE_Rev_K.pdf), <https://github.com/OLIMEX/ESP32-POE/blob/master/DOCUMENTS/ESP32-POE-user-manual.pdf>
    
    <figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"imageId":"6770cbdcf3117"}" data-wp-interactive="core/image">![Pinout documentation for the ESP32-POE-GPIO, from https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/resources/ESP32-POE-GPIO.png](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/12/ESP32-POE-GPIO.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Pinout documentation for the ESP32-POE-GPIO, from https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/resources/ESP32-POE-GPIO.png" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure>
    - For some reason, not getting power from USB, but PoE is ok 
        - Just noted this… ominous… 
            - ***Important notice:** ESP32-POE has **no galvano isolation** from Ethernet’s power supply, when you program the board via the micro USB connector the Ethernet cable should be disconnected (if you have power over the Ethernet cable)! Consider using Olimex USB-ISO to protect your computer and board from accidental short circuit. Also consider instead using Olimex ESP32-PoE-ISO board which is insulated.*
            - Need to find another way to power the board when programming…
            - There’s a LiPo JST connector! 
                - Which can be charged by Ethernet
            - Maybe I just need to work out what’s wrong with my cable… 
                - Ok, the first one was charge-only, it’s now labelled as such
                - The second one works better, but cannot be fully inserted into the socket… I don’t think I have a single non-dodgy micro-USB cable anymore 
                    - I found one that works. It’s ominously labelled “Dodgy?”
        - I got a few programs loaded on [ESP32-POE](https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/open-source-hardware), and it looks fine
    - Using the water sensor on the ESP32-POE 
        - The AnalogRead demo is mostly there
        - Need to work out which port to use 
            - It would be nice to be able to use the UEXT header 
                - I’ll have to try with the +3.3V from the header, otherwise I’ll have to source the POE power from somewhere else
                - 36 fits the bill
    - Next step: can I use +3.3v from UEXT, or +5v on the side to drive the current loop sensor?
    - To-read list for next time: trying ESP home 
        - <https://esphome.io/components/sensor/adc>
        - <https://www.pieterbrinkman.com/2022/02/02/build-a-cheap-water-usage-sensor-using-esphome-home-assistant-and-a-proximity-sensor/>
        - <https://www.pieterbrinkman.com/2022/01/01/2022-update-flash-esphome-on-esp32-esp2866-nodemcu-board/>
        - <https://github.com/esphome/esphome-flasher/releases>
    
    </div>

<nav aria-label="Pagination" class="wp-block-query-pagination is-layout-flex wp-block-query-pagination-is-layout-flex"><div class="wp-block-query-pagination-numbers"><span aria-current="page" class="page-numbers current">1</span>[2](?query-7-page=2&type=jekyll)[3](?query-7-page=3&type=jekyll)[4](?query-7-page=4&type=jekyll)</div>[Next Page](/wp-admin/export.php?type=jekyll&query-7-page=2)</nav></div>