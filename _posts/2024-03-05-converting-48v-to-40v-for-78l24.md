---
id: 1413
title: 'Converting 48v to 40v for 78L24'
date: '2024-03-05T16:14:10+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1413'
permalink: /2024/03/05/converting-48v-to-40v-for-78l24/
activitypub_status:
    - federated
iawp_total_views:
    - '1'
categories:
    - electronics
    - µblog
tags:
    - ESP32
    - ESPHome
    - 'water tank sensor'
format: status
---

- I got pretty much all my components wrong to power my[ ](https://blog.narf.ssji.net/2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/)[4–20mA Current Loop Rain Water Tank Sensor](https://blog.narf.ssji.net/2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/): PNP instead of NPN transistor, and non-power components (I may be able to get away with this one) 
    - Though I should be able to swap the VCC and GND in the circuit and get the PNP to work
- Other suggestions to test (and be more careful about component selection): 
    - <https://electronics.stackexchange.com/questions/497271/converting-48-vdc-to-24-vdc>
    - <https://electronics.stackexchange.com/a/497274>
        - zener + to220/darlington
        - buck converter TPS40200 <https://www.ti.com/lit/ds/symlink/tps40200.pdf>
    - more zener: <https://electronics.stackexchange.com/questions/461834/simplest-way-to-reduce-voltage-from-48v-to-36v> <https://electronics.stackexchange.com/a/461841>
        - 1n4740a + tip122 to220 + 2.2k

<div class="wp-block-image"><figure class="aligncenter size-full is-resized">[![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/y5OFL.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/y5OFL.png)<figcaption class="wp-element-caption">Source: <https://electronics.stackexchange.com/a/497274></figcaption></figure></div>- It also looks like I fried the ESP32-POE when I put the incorrectly-powered (48V rather than 24V ) 4-20mA sensor in the loop, and had too high voltage going into the ADC 
    - ESP32 can measure a max of about 2.4V with `ADC_ATTEN_DB_12` attenuation <https://docs.espressif.com/projects/esp-idf/en/release-v4.4/esp32/api-reference/peripherals/adc.html>
        - this can be controlled in ESPHome, too <https://esphome.io/components/sensor/adc.html#esp32-attenuation>, but reports up to 3.12V max range in `auto` mode
    - Alan suggested adding a 470Ω resistor from the input and two clamping diodes to keep the voltage within the range of the ADC

<div class="wp-block-image"><figure class="aligncenter size-full">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/image_480.png)</figure></div>