---
id: 1254
title: Off-by-one
date: '2024-01-16T00:29:31+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1254'
permalink: '/?p=1254'
---

- Found an annotated list programming guide for the 2m [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/) by VK2KJF: [http://www.unixsupport.com.au/hamradio/radios/awa/rt85/RT85\_Manuals/AWA\_RT85\_programming-part4.pdf](http://www.unixsupport.com.au/hamradio/radios/awa/rt85/RT85_Manuals/AWA_RT85_programming-part4.pdf)
- Realised I had an off-by-one error between the frequencies and the dumped codes in the EEPROM 
    - Which means I was wrong about where channel 0 is. Channel 0 is… at index 0
- There is generally a gap of `0x5` or `0xA` between programmed frequencies, 
    - This lines up with a 25/50kHz gap and the 5kHz channel width (also *f<sub>ref</sub>*)
    - This is not always the case, even if the MSB (`0xC0`—`0xC6`) doesn’t change
- RX and TX frequencies aren’t encoded in the same way 
    - simplex channels have different values,
    - *e.g.*, 146.450MHz is `0xC332` RX but `0xC4AA` TX

<figure class="wp-block-image size-full">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/image-1.png)</figure>