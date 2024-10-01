---
id: 1539
title: 'Random discoveries'
date: '2024-05-04T17:03:52+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1539'
permalink: /2024/05/04/random-discoveries/
activitypub_status:
    - federated
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
categories:
    - DIY
    - electronics
    - µblog
tags:
    - 'AWA RT85'
    - 'water tank sensor'
format: status
---

- Olimex now has the ESP32-POE2 <https://www.olimex.com/Products/IoT/ESP32/ESP32-POE2/open-source-hardware>, which has a nice configurable 12/24V line that would make it substantially easier to build my [water tank sensor](https://blog.narf.ssji.net/tag/water-tank-sensor/). Waiting for Mouser to carry it.
- I finally settled for EH connectors for the CTCSS module for my [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/). They were surprisingly hard to find. I eventually worked out that DigiKey had them. Everything about ordering from DigiKey was tedious, and I’m not even sure my order will go through as it looked like the payment failed… But I got a confirmation email anyway. Who knows? 
    - I also found a basic Kicad model for an ATMEGA-328P PCB <https://github.com/trentfowler/atmega328p>, but the PCB is SMD rather. I’ll start with a prototyping board, but I should be able to reuse the schematics to make a through-hole PCB for the DIP version that I have instead.