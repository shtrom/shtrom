---
id: 1106
title: 'Switching to ESP32'
date: '2023-12-29T00:05:44+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1106'
permalink: /2023/12/29/switching-to-esp32/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
image: /wp-content/uploads/sites/3/2023/12/ESP32-POE-GPIO.png
categories:
    - electronics
    - µblog
tags:
    - Arduino
    - ESP32
    - 'water tank sensor'
format: status
---

- Order from Mouser arrived, with a replacement Atmega 328, and a selection of ESP32 boards
- Duemilanove still fails to program with the same error as before on the new Atmega 
    - So I borked the dev board
    - But I might have two functional Atmega \\o/
- Playing with the [ESP32-POE](https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/open-source-hardware)
    - I also ordered an -IND for the real deployment
    - Docs: <https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/resources/ESP32-POE-GPIO.png>, [https://github.com/OLIMEX/ESP32-POE/blob/master/HARDWARE/ESP32-PoE-hardware-revision-K/ESP32-PoE\_Rev\_K.pdf](https://github.com/OLIMEX/ESP32-POE/blob/master/HARDWARE/ESP32-PoE-hardware-revision-K/ESP32-PoE_Rev_K.pdf), <https://github.com/OLIMEX/ESP32-POE/blob/master/DOCUMENTS/ESP32-POE-user-manual.pdf>

<figure class="wp-block-image size-full wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2023\/12\/ESP32-POE-GPIO.png","figureClassNames":"wp-block-image size-full","figureStyles":null,"imgClassNames":"wp-image-1107","imgStyles":null,"targetWidth":1920,"targetHeight":1280,"scaleAttr":false,"ariaLabel":"Enlarge image: Pinout documentation for the ESP32-POE-GPIO, from https:\/\/www.olimex.com\/Products\/IoT\/ESP32\/ESP32-POE\/resources\/ESP32-POE-GPIO.png","alt":"Pinout documentation for the ESP32-POE-GPIO, from https:\/\/www.olimex.com\/Products\/IoT\/ESP32\/ESP32-POE\/resources\/ESP32-POE-GPIO.png"}" data-wp-interactive="core/image">![Pinout documentation for the ESP32-POE-GPIO, from https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/resources/ESP32-POE-GPIO.png](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/12/ESP32-POE-GPIO.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Pinout documentation for the ESP32-POE-GPIO, from https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/resources/ESP32-POE-GPIO.png" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure>- For some reason, not getting power from USB, but PoE is ok 
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