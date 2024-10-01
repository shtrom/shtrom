---
id: 1351
title: 'Adding CTCSS tones'
date: '2024-02-07T00:35:07+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1351'
permalink: '/?p=1351'
---

- Need to add tones 
    - [http://www.pa3guo.com/PA3GUO\_Arduino\_CTCSS\_v1.2.pdf](http://www.pa3guo.com/PA3GUO_Arduino_CTCSS_v1.2.pdf) use PWM with varying duty cycle into a bandpass to generate the desired tone 
        - Arduino/ATMEGA <https://github.com/tczerwonka/arduino-ctcss>
    - No 91.5 in RT85 programming map, map to 0/no-tone? 
        - WIA default standard tones <https://www.wia.org.au/members/bandplans/data/>
        - just transmit 91.5 instead of no tone
- ATMEGA128 install without dev board https://electronics.stackexchange.com/a/53719 
    - Can take 3 to 5V for Vcc, max 200mA
    - or just reuse the dev board… again 
        - Arduino builds bins and hex (with and without bootloader) in `/tmp/arduino_build_`\*
        - Can flash the ATMEGA with the T48 programmer
        - Blink runs, but every 19s rather than 1s 
            - same as <https://forum.arduino.cc/t/a-very-strange-issue-led-blink-too-slowly/331926/7>
            - Xgpro can set fuses (didn’t check with minipro)
            - Arduino fuse settings here: <https://www.martyncurrey.com/arduino-atmega-328p-fuse-settings/>
                - works! and that fixed in-situ programming

<figure class="wp-block-image size-full">![Arduino Duemilanove or Nano w/ ATmega328 Default Fuse Settings, from https://www.martyncurrey.com/arduino-atmega-328p-fuse-settings/](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/Screenshot-from-2024-02-07-00-31-12.png)</figure>