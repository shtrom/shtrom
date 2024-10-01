---
id: 1347
title: 'Adding CTCSS tones with an Arduino'
date: '2024-02-07T00:35:07+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1347'
permalink: /2024/02/07/adding-ctcss-toness-arduino/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
activitypub_status:
    - federated
iawp_total_views:
    - '18'
image: /wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-08-47-38.png
categories:
    - electronics
    - ham
    - µblog
tags:
    - Arduino
    - 'AWA RT85'
    - 'Xgecu T48'
format: status
---

- Need to add tones to the [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/)
    - [http://www.pa3guo.com/PA3GUO\_Arduino\_CTCSS\_v1.2.pdf](http://www.pa3guo.com/PA3GUO_Arduino_CTCSS_v1.2.pdf) use PWM with varying duty cycle into a bandpass to generate the desired tone 
        - Arduino/ATMEGA <https://github.com/tczerwonka/arduino-ctcss>
    - No 91.5 in RT85 programming map, map to 0/no-tone? 
        - WIA default standard tones <https://www.wia.org.au/members/bandplans/data/>
        - just transmit 91.5 instead of no tone
- ATMEGA128 install without dev board <https://electronics.stackexchange.com/a/53719>
    - Can take 3 to 5V for Vcc, max 200mA
    - or just reuse the dev board… again 
        - Arduino builds `bin`s and `hex` (with and without bootloader) in `/tmp/arduino_build_`\*
        - Can flash the ATMEGA with the T48 programmer
        - `Blink.ino` runs, but every ~19s rather than 1s 
            - same as <https://forum.arduino.cc/t/a-very-strange-issue-led-blink-too-slowly/331926/7>; the ATGEMA328’s fuses aren’t set right for Arduino usage
            - Xgpro can set fuses (didn’t check with minipro)
            - Arduino fuse settings here: <https://www.martyncurrey.com/arduino-atmega-328p-fuse-settings/>
                - works! and that fixed in-situ programming 
                    - my Arduino board was not dead after all!

<figure class="wp-block-gallery has-nested-images columns-2 wp-block-gallery-14 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">[![Table of CTCSS tones that can be programmed from the EPROM of the AWA RT85](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-08-59-21.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-08-59-21.png)</figure><figure class="wp-block-image size-large">[![Arduino Duemilanove or Nano w/ ATmega328 Default Fuse Settings, from https://www.martyncurrey.com/arduino-atmega-328p-fuse-settings/](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-00-31-12.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-00-31-12.png)</figure><figure class="wp-block-image size-large">[![Screenshot of Xgpro showing the fuse settings for an ATMEGA328 to be used as an Arduino](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-08-47-38.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-08-47-38.png)</figure></figure>