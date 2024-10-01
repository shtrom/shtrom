---
id: 1076
title: 'Updating channel memory on decommisioned AWA RT85 radios'
date: '2023-11-25T23:15:42+11:00'
author: 'Olivier Mehani'
excerpt: 'I have an AWA RT85 2m radio, programmed for VK2 Ham channels. Now in VK7, I''m working on reprogramming it, by finding how and what to write to its EPROM.'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1076'
permalink: '/?p=1076'
---

Shortly after getting my amateur radio license, I bought an old [AWA RT85 2m radio](https://www.qsl.net/vk3byy/rt85/index.html) from my club. It was already programmed for the local (VK2) repeaters, and all was good. Then I moved interstate, and the radio has been collecting the proverbial dust ever since.  
  
I recently decided to get it back in service, which mainly means reprogramming it to local (VK7) channels.

[µblog](https://blog.narf.ssji.net/category/%c2%b5blog/) tag: [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/)

<div class="wp-block-jetpack-tiled-gallery aligncenter is-style-rectangular"><div class="tiled-gallery__gallery"><div class="tiled-gallery__row"><div class="tiled-gallery__col" style="flex-basis:63.96477%"><figure class="tiled-gallery__item">![An AWA RT85 radio](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231125_110150359.MP_-1024x768.jpg?ssl=1)</figure></div><div class="tiled-gallery__col" style="flex-basis:36.03523%"><figure class="tiled-gallery__item">![](https://i1.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231125_110243594-768x1024.jpg?ssl=1)</figure></div></div></div></div>Progress so far:

- It uses an [NMC27C16Q-45](https://www.silicon-ark.co.uk/datasheets/27c16%20datasheet%20national.pdf)
- Bought an [XGecu T48](http://www.xgecu.com/en/) [from sunwenjun on eBay](https://www.ebay.com.au/itm/225060789109), based on info on <https://proghq.org/wiki/index.php/TL866>
    - Unfortunately, the T48 is a new version, not currently supported by the [Open-TL866 firmware](https://github.com/JohnDMcMaster/open-tl866), nor current by [minipro](https://gitlab.com/DavidGriffith/minipro/)
        - There is a [WiP branch](https://gitlab.com/anarsoul/minipro/-/tree/t48-wip?ref_type=heads) to [support the T48 in minipro](https://gitlab.com/DavidGriffith/minipro/-/issues/270)
    - In the meantime, the [Xgecu Windows programming tool](https://www.mediafire.com/file/r5y2lcs8vkl2bjz/XgproV1263_Setup.rar/file) [works in Wine](https://spun.io/2018/07/04/using-the-xgecu-tl866ii-plus-under-linux-with-wine/)
        - It needs a [replacement setupapi.dll to work](https://github.com/radiomanV/TL866/tree/master/wine)
- Want an EEPROM to avoid UV erasing 
    - The [AT28C16](http://cva.stanford.edu/classes/cs99s/datasheets/at28c16.pdf) [is compatible](https://pinside.com/pinball/forum/topic/28c16-eeprom-replacement-for-2716-eprom)
    - Took a chance on [a pair on eBay](https://www.ebay.com.au/itm/403083082728?hash=item5dd99fbbe8:g:ctUAAOSwj4JbbX3S&amdata=enc%3AAQAIAAAA4NXNOOM4JV8UGh%2Bg1%2FIZKa5ky28y7uL64XfJvvtvuxWY88zW0y9iVtipSoiWdjx7Z8XoFks5vSF1eJV98lVgu87so4CAdA7m%2BLdm7%2Fm0oUU2hjk0V5ZhM28ISjwhjMYAUZ1oSYRgYXnXpyrNRVSrq5UPrQmXSDV7QyzukZoLAogSTtKfY%2FRUu9Dj2UXkOjmtEv0yaPCxopvvcxh%2BDQZfn3xqIuD829zK8t%2F1pJIm73SIYuWlBqbFm4LkP7ixSOsO1A9R%2BGzRCU7KWm9YBqNBWy0yWFNkxRU%2BkVcHVuKmFZHg%7Ctkp%3ABFBM0t3G4YBj)