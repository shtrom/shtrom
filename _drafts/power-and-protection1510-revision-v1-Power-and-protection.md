---
id: 1521
title: 'Power and protection'
date: '2024-04-08T00:17:15+10:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1521'
permalink: '/?p=1521'
---

- More work on the [4–20mA Current Loop Rain Water Tank Sensor](https://blog.narf.ssji.net/2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/)
- Need to drop the voltage for the 78L24 
    - 46 to 24 -&gt; 22V 
        - Drop 11V in each stage -&gt; 11V zener 
            - Splitting voltage drop to dissipate power equally in each component
            - Current control resistor: 5mA at 46V (before established regime): ~10k
- Need to protect the ADC input 
    - Two Schottkys to Vref <https://www.analog.com/en/resources/technical-articles/protecting-adc-inputs.html>
        - What values? 
            - Do Schottkys have values?
            - BAT54S 
                - Only SMD <https://diotec.com/request/datasheet/bat54.pdf>
    - Or just one 3.3v Zener? 
        - Will keep as a backup
- Might as well make a PCB 
    - Adding a header for various bypasses

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-134 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-full">[![Electronic diagram of voltage drop, sensing and ADC input stages for a 4--20mA current-loop sensor](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/04/image-2.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/04/image-2.png)</figure><figure class="wp-block-image size-large">[![PCB for the voltage drop, sensing and ADC input stages for a 4--20mA current-loop sensor](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/04/image-1024x429.png)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/04/image.png)</figure></figure>