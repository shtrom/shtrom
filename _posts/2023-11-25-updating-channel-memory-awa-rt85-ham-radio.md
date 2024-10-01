---
id: 1067
title: 'Updating channel memory on decommissioned AWA RT85 radio'
date: '2023-11-25T23:15:42+11:00'
author: 'Olivier Mehani'
excerpt: 'I have an AWA RT85 2m radio, programmed for VK2 Ham channels. Now in VK7, I''m working on reprogramming it, by finding how and what to write to its EPROM.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1067'
permalink: /2023/11/25/updating-channel-memory-awa-rt85-ham-radio/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '1'
image: /wp-content/uploads/sites/3/2023/11/PXL_20231125_110150359.MP_-scaled.jpg
categories:
    - electronics
    - ham
    - hardware
    - µblog
tags:
    - 'AWA RT85'
    - minipro
    - 'Xgecu T48'
---

Shortly after getting my amateur radio license, I bought an old [AWA RT85 2m radio](https://www.qsl.net/vk3byy/rt85/index.html) from my club. It was already programmed for the local (VK2) repeaters, and all was good. Then I moved interstate, and the radio has been collecting the proverbial dust ever since.  
  
I recently decided to get it back in service, which mainly means reprogramming it to local (VK7) channels.

[µblog](https://blog.narf.ssji.net/category/%c2%b5blog/) tag: [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/)

<div class="wp-block-jetpack-tiled-gallery aligncenter is-style-rectangular"><div class="tiled-gallery__gallery"><div class="tiled-gallery__row"><div class="tiled-gallery__col" style="flex-basis:63.96477%"><figure class="tiled-gallery__item">![An AWA RT85 radio](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231125_110150359.MP_-1024x768.jpg?ssl=1)</figure></div><div class="tiled-gallery__col" style="flex-basis:36.03523%"><figure class="tiled-gallery__item">![](https://i1.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/PXL_20231125_110243594-768x1024.jpg?ssl=1)</figure></div></div></div></div># Progress so far

- It uses an [NMC27C16Q-45](https://www.silicon-ark.co.uk/datasheets/27c16%20datasheet%20national.pdf)
- Bought an [XGecu T48](http://www.xgecu.com/en/) [from sunwenjun on eBay](https://www.ebay.com.au/itm/225060789109), based on info on <https://proghq.org/wiki/index.php/TL866>
    - Unfortunately, the T48 is a new version, not currently supported by the [Open-TL866 firmware](https://github.com/JohnDMcMaster/open-tl866), nor current by [minipro](https://gitlab.com/DavidGriffith/minipro/)
        - There is a [WiP branch](https://gitlab.com/anarsoul/minipro/-/tree/t48-wip?ref_type=heads) to [support the T48 in minipro](https://gitlab.com/DavidGriffith/minipro/-/issues/270)
    - In the meantime, the [Xgecu Windows programming tool](https://www.mediafire.com/file/r5y2lcs8vkl2bjz/XgproV1263_Setup.rar/file) [works in Wine](https://spun.io/2018/07/04/using-the-xgecu-tl866ii-plus-under-linux-with-wine/)
        - It needs a [replacement setupapi.dll to work](https://github.com/radiomanV/TL866/tree/master/wine)
- Want an EEPROM to avoid UV erasing 
    - The [AT28C16](http://cva.stanford.edu/classes/cs99s/datasheets/at28c16.pdf) [is compatible](https://pinside.com/pinball/forum/topic/28c16-eeprom-replacement-for-2716-eprom)
    - Took a chance on [a pair on eBay](https://www.ebay.com.au/itm/403083082728?hash=item5dd99fbbe8:g:ctUAAOSwj4JbbX3S&amdata=enc%3AAQAIAAAA4NXNOOM4JV8UGh%2Bg1%2FIZKa5ky28y7uL64XfJvvtvuxWY88zW0y9iVtipSoiWdjx7Z8XoFks5vSF1eJV98lVgu87so4CAdA7m%2BLdm7%2Fm0oUU2hjk0V5ZhM28ISjwhjMYAUZ1oSYRgYXnXpyrNRVSrq5UPrQmXSDV7QyzukZoLAogSTtKfY%2FRUu9Dj2UXkOjmtEv0yaPCxopvvcxh%2BDQZfn3xqIuD829zK8t%2F1pJIm73SIYuWlBqbFm4LkP7ixSOsO1A9R%2BGzRCU7KWm9YBqNBWy0yWFNkxRU%2BkVcHVuKmFZHg%7Ctkp%3ABFBM0t3G4YBj)

<div class="wp-block-query is-layout-flow wp-block-query-is-layout-flow">- <div class="wp-block-columns is-layout-flex wp-container-core-columns-is-layout-4 wp-block-columns-is-layout-flex"><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:66.66%">### Updating channel memory on decommissioned AWA RT85 radio
    
    </div><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:33.33%"><div class="has-text-align-right wp-block-post-date"><time datetime="2023-11-25T23:15:42+11:00">2023-11-25</time></div></div></div><div class="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow">Shortly after getting my amateur radio license, I bought an old [AWA RT85 2m radio](https://www.qsl.net/vk3byy/rt85/index.html) from my club. It was already programmed for the local (VK2) repeaters, and all was good. Then I moved interstate, and the radio has been collecting the proverbial dust ever since.  
      
    I recently decided to get it back in service, which mainly means reprogramming it to local (VK7) channels.
    
    [µblog](https://blog.narf.ssji.net/category/%c2%b5blog/) tag: [AWA RT85](https://blog.narf.ssji.net/tag/awa-rt85/)
    
     [<span aria-label="Continue reading Updating channel memory on decommissioned AWA RT85 radio">(more…)</span>](https://blog.narf.ssji.net/2023/11/25/updating-channel-memory-awa-rt85-ham-radio/#more-1067)</div>
- <div class="wp-block-columns is-layout-flex wp-container-core-columns-is-layout-5 wp-block-columns-is-layout-flex"><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:66.66%">### To desolder a chip
    
    </div><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:33.33%"><div class="has-text-align-right wp-block-post-date"><time datetime="2023-12-26T20:33:19+11:00">2023-12-26</time></div></div></div><div class="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow">Back onto the [RT85 programming](https://blog.narf.ssji.net/2023/11/25/updating-channel-memory-awa-rt85-ham-radio/), I tried to desolder the 27C16 EPROM from the Z-273 module that carries it. I went down the path of the solder wick, but didn’t have much success making the chip move despite a lot of solder being removed.
    
    Being as equipped as I usually am, akin to from a second-hand budget store, I don’t have a hot air rework station. According to [this video](https://www.youtube.com/watch?app=desktop&v=fb7iWSXNta4), I may be able to get away with an el-cheapo all-purpose hot air gun from Bunnings, and a beer tin to fashion a nozzle out of. I’ll give that a go.
    
    On unrelated matters, does anyone have the personality details of a RT85A data reprogrammed to the 2m Ham bands? Asking for a friend who might need it very soon.
    
     [<span aria-label="Continue reading To desolder a chip">(more…)</span>](https://blog.narf.ssji.net/2023/12/26/to-desolder-a-chip/#more-1092)</div>
- <div class="wp-block-columns is-layout-flex wp-container-core-columns-is-layout-6 wp-block-columns-is-layout-flex"><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:66.66%">### EPROM switcharoo
    
    </div><div class="wp-block-column is-layout-flow wp-block-column-is-layout-flow" style="flex-basis:33.33%"><div class="has-text-align-right wp-block-post-date"><time datetime="2023-12-31T01:24:45+11:00">2023-12-31</time></div></div></div><div class="entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow">
    - Working on [Updating channel memory on decommissioned AWA RT85 radio](https://blog.narf.ssji.net/2023/11/25/updating-channel-memory-awa-rt85-ham-radio/)
    - Managed to desolder the original MC27C16 EPROM 
        - The heat gun approach worked a treat, particularly as it had a 50-450°C range, so I could avoid overheating the board with only 150–200°C
    - Dumped the EPROM data, and re-loaded it on an AT28C16
    - Put a DIP24 socket in the daughter board, and the 28C16 in it 
        - It’s a snug fit, but it’s a fit
    - Realised that I didn’t have an RT85A, but an original RT85, according to <https://www.qsl.net/vk3byy/rt85/rt85data.html> (VK3BYY) 
        - There is an archive.org of a page from VK3TAE about it <https://web.archive.org/web/20100618044202/http://www.users.on.net/~gbear/rt85.html>, and particularly the [programming data](https://web.archive.org/web/20050615023352/http://keycom.d2.net.au/rt85.pdf) (took copies for later reference)
        - At a glance, the programming data matches what’s in the EEPROM
    
    [<span aria-label="Continue reading EPROM switcharoo">(more…)</span>](https://blog.narf.ssji.net/2023/12/31/eprom-switcharoo/#more-1115)</div>

<nav aria-label="Pagination" class="wp-block-query-pagination is-layout-flex wp-block-query-pagination-is-layout-flex"><div class="wp-block-query-pagination-numbers"><span aria-current="page" class="page-numbers current">1</span>[2](?query-7-page=2&type=jekyll)[3](?query-7-page=3&type=jekyll)<span class="page-numbers dots">…</span>[5](?query-7-page=5&type=jekyll)</div>[Next Page](/wp-admin/export.php?type=jekyll&query-7-page=2)</nav></div>