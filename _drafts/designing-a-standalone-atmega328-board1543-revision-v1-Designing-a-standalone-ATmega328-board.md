---
id: 1548
title: 'Designing a standalone ATmega328 board'
date: '2024-05-07T00:51:17+10:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1548'
permalink: '/?p=1548'
---

- For the [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/) CTCSS circuit
- [https://circuitstate.com/wp-content/uploads/2023/01/ATmega328P-28-DIP-Pinout-Diagram-Rev-0.5-CIRCUITSTATE-Electronics-1\_1.png](https://circuitstate.com/wp-content/uploads/2023/01/ATmega328P-28-DIP-Pinout-Diagram-Rev-0.5-CIRCUITSTATE-Electronics-1_1.png)
- VCC and AVCC to 5V 
    - AVCC for analog measurement
    - Don’t connect AREF! <https://forum.arduino.cc/t/what-is-avcc-for-on-the-atmega328/66423/6>
- 5V available from P903 (pin 1), and ~10V from P358 (pin 8) 
    - adding optional LM7805 if needed

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-136 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">[![A diagram summarising the pinout of the ATmega328p, from https://circuitstate.com/wp-content/uploads/2023/01/ATmega328P-28-DIP-Pinout-Diagram-Rev-0.5-CIRCUITSTATE-Electronics-1_1.png](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/05/ATmega328P-28-DIP-Pinout-Diagram-Rev-0.5-CIRCUITSTATE-Electronics-1_1-1024x717.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/05/ATmega328P-28-DIP-Pinout-Diagram-Rev-0.5-CIRCUITSTATE-Electronics-1_1.png)</figure><figure class="wp-block-image size-large">[![Render of the PCB for a CTCSS-generation circuit based on an ATmega328p, LM7805 and discrete component filter](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/05/ctcss_circuit-1024x546.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/05/ctcss_circuit.png)</figure></figure>