---
id: 1091
title: 'To kill a chip'
date: '2023-12-16T00:04:13+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1091'
permalink: '/?p=1091'
---

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

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-32 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">![Screenshot of Xgpro running in Wine](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/12/image-1024x576.png)<figcaption class="wp-element-caption">Using Xgpro in Wine with anXgecu T48 to test an ATMEGA328P. The chip seems dead…</figcaption></figure></figure>- Looks like I’m gonna have to get a new microcontroller… 
    - This is an opportunity to widen the search 
        - The ESP32-POE(-IND) could be a good fit <https://www.olimex.com/Products/IoT/ESP32/ESP32-POE/open-source-hardware> <https://au.mouser.com/ProductDetail/Olimex-Ltd/ESP32-POE?qs=unwgFEO1A6tUQVMxdOBsBw%3D%3D >
            - Could save dev time by using <https://esphome.io/ > <https://mastodon.social/@flameeyes/111360625680537907>