---
id: 1338
title: 'Voltage drop'
date: '2024-01-26T19:30:28+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1338'
permalink: '/?p=1338'
---

- Need to drop voltage from 46V to 24V for the [4–20mA Current Loop Rain Water Tank Sensor](https://blog.narf.ssji.net/2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/)
- Can use L7824 <https://au.mouser.com/datasheet/2/389/l78-1849632.pdf>
    - Max 40V input
- Or use a Buck Converter, e.g., TPS40200[ https://electronics.stackexchange.com/a/497283](< https://electronics.stackexchange.com/a/497283>)
    - <https://www.ti.com/lit/ds/symlink/tps40200.pdf?ts=1705842644442>
- The L7824 datasheet suggests an emitter-follower zener regulator on the input 
    - <https://www.eeeguide.com/emitter-follower-voltage-regulator/>

<div class="wp-block-jetpack-tiled-gallery aligncenter is-style-rectangular"><div class="tiled-gallery__gallery"><div class="tiled-gallery__row"><div class="tiled-gallery__col" style="flex-basis:100.00000%"><figure class="tiled-gallery__item">[![A high input voltage circuit from the datasheet of the L78xx voltage regulators.](https://i1.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/image-3.png?ssl=1)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/image-3.png)</figure></div></div><div class="tiled-gallery__row"><div class="tiled-gallery__col" style="flex-basis:100.00000%"><figure class="tiled-gallery__item">[![A high input voltage circuit from the datasheet of the L78xx voltage regulators.](https://i1.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/image-2.png?ssl=1)](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/image-2.png)</figure></div></div></div></div>