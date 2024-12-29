---
id: 1710
title: ESP32-POE-two-
date: '2024-11-09T19:02:44+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1710'
permalink: '/?p=1710'
---

- Mouser added the ESP32-POE2 to their catalogue, but with no stock 
    - Ended up ordering straight from Olimex <https://www.olimex.com/Products/IoT/ESP32/ESP32-POE2/open-source-hardware>
- Playing around with esphome, it seems to work with the same config as the esp32-poe 
    - the EXT1 header has both VPP (my 24v), and GPIO36 (my ADC) <https://github.com/OLIMEX/ESP32-POE2/blob/main/DOCUMENTS/ESP32-POE2-user-manual.pdf>
        - VPP@1
        - GND@2,4,6,8
        - GPIO36@12
    - some doc on ESP32 ADCs <https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/>
- TODO: 
    - get the right multiplier for the VCC measurements on GPIO35 
        - should be ca. 3.3V
        - `filters[0].multiply`=20?
    - set up VPP to 24V
    - make an adapter for EXT1, including the necessary port protection, this time…
    - calibrate the sensor / GPIO36 
        - <https://esphome.io/components/sensor/#sensor-filters>

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-139 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">![Pinout of the EXT1 connector of the esp32-poe2](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/11/Screenshot-From-2024-11-09-18-37-17-1024x547.png)</figure><figure class="wp-block-image size-large">![Screenshot of a terminal showing a successful run of `esphome run water-tank-sensor.yaml`](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/11/Screenshot-From-2024-11-09-18-36-55.png)</figure></figure>