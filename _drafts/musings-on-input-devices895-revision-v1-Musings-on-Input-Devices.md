---
id: 1412
title: 'Musings on Input Devices'
date: '2024-03-01T16:33:58+11:00'
author: 'Olivier Mehani'
excerpt: 'My main input devices are an Ergodox with blank keycaps in a Dvorak layout, and an Evoluent Vertical Mouse. My mobile uses a 9-keys swipe-based keyboard (MessageEase until recently, now Thumb-Key with a compatible layout). People sometimes ask me about this, and then I talk to them for way longer than they signed up for. Perhaps a written summary would save some in the future (but do ask if you want a chat!).'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1412'
permalink: '/?p=1412'
---

My main input devices are an [Ergodox](https://www.ergodox.io/) with blank keycaps in a [Dvorak layout](https://en.wikipedia.org/wiki/Dvorak_keyboard_layout), and an [Evoluent Vertical Mouse](https://evoluent.com/products/vm4r/). My mobile uses a 9-keys swipe-based keyboard ([MessageEase](https://www.exideas.com/ME/index.php) until recently, now [Thumb-Key](https://f-droid.org/packages/com.dessalines.thumbkey/) with a compatible layout). People sometimes ask me about this, and then I talk to them for way longer than they signed up for. Perhaps a written summary would save some in the future (but do ask if you want a chat!).

tl;dr:

- Good hand alternation and minimal finger movement / stretch helped squash my RSI 
    - Using wrist-cuff leveling pads ([Wristease](http://wristease.com/)) helped more than keyboard- or desk-attached wirst pads
- A good keyboard layout, such as Dvorak, is important 
    - Switching to very different layouts takes time. 
        - Be prepared, and choose the target layout wisely. The cost of switching vs. the benefit of the target layout need to be weighted against the time to become as proficient with it as the previous layout.
- *However*, it doesn’t matter anywhere near as much as the form factor of the keyboard (ortholinear, split, …). 
    - Particularly, having modifier keys in symmetrical locations for each hands really supports hand alternation.
    - Having other useful keys such as `Backspace` or `Enter` in a column in the middle is very convenient.
- Other input systems are also worth reviewing, particularly mobile phone input methods. They are quite different from desktop entry, and have a different set of constraints which drastically alters the solution space. Simply copying physical keyboards is far from optimal.

<div class="wp-block-image"><figure class="aligncenter size-large is-resized wp-lightbox-container" data-wp-context="{"uploadedSrc":"https:\/\/blog.narf.ssji.net\/wp-content\/uploads\/sites\/3\/2024\/02\/signal-2024-02-24-191001.jpeg","figureClassNames":"aligncenter size-large is-resized","figureStyles":null,"imgClassNames":"wp-image-1370","imgStyles":"width:562px;height:auto","targetWidth":2048,"targetHeight":1536,"scaleAttr":false,"ariaLabel":"Enlarge image: An split ortholinear keboard (Ergodox) with blank keycaps except for a red Esc key on the top left index finger; a mobile in the middle showing a 3x3 swipe keyboard (ThumbKey), and a vertical mouse (Evoluent VM4R) on the right.","alt":"An split ortholinear keboard (Ergodox) with blank keycaps except for a red Esc key on the top left index finger; a mobile in the middle showing a 3x3 swipe keyboard (ThumbKey), and a vertical mouse (Evoluent VM4R) on the right."}" data-wp-interactive="core/image">![An split ortholinear keboard (Ergodox) with blank keycaps except for a red Esc key on the top left index finger; a mobile in the middle showing a 3x3 swipe keyboard (ThumbKey), and a vertical mouse (Evoluent VM4R) on the right.](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/signal-2024-02-24-191001.jpeg?fit=770%2C578&ssl=1)<button aria-haspopup="dialog" aria-label="Enlarge image: An split ortholinear keboard (Ergodox) with blank keycaps except for a red Esc key on the top left index finger; a mobile in the middle showing a 3x3 swipe keyboard (ThumbKey), and a vertical mouse (Evoluent VM4R) on the right." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="context.imageButtonRight" data-wp-style--top="context.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></div># Physical keyboards

I started using computers with plain French AZERTY keyboards. Around the time when I got serious with Unix machines and programming, I switched to a QWERTY layout. I quickly realised that, to remain a typographical pedant, I needed to type accents properly, and found that the X11 `intl` variant was my preference to type any number of non-ASCII characters with a few dead key modifiers.

## TypeMatrix

At some point, I heard about the [TypeMatrix keyboard](http://typematrix.com/2030/features.php), which sounded interesting from a form factor perspective. The main selling point was that the columns weren’t staggered, which held promises to squash nascent RSI symptoms (sore forearms and finger tingles).

<div class="wp-block-image is-style-default"><figure class="aligncenter size-full is-resized">![Top view of a TypeMatrix 2030 keyboard, from http://typematrix.com/2030/gallery.php](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/tmx-2030_gallery-1.png?fit=900%2C405&ssl=1)<figcaption class="wp-element-caption">Source: <http://typematrix.com/2030/gallery.php></figcaption></figure></div>This felt like an improvement, but two other features stood out more to me. It was surprisingly good to have double-height shift and control keys, as they give a larger target to mash with the pinkies without having to be too precise. I discovered that their left/right symmetrical position was also quite important to help hand-alternation when chording shortcuts (e.g., Right `Ctrl` + Left `V`). The most useful feature, however, is the column in the middle of the alpha-numeric keys. In addition to providing a better visual separation for each hand, it also allows to reach common keys, `Del`, `Backspace` and `Enter` from either hand with the index finger, similarly to the space bar reachable from both thumbs, rather than only available to the right pinky.

## Dvorak layout

Another feature of the TypeMatrix is a one-key hardware switch to a [Dvorak layout](https://en.wikipedia.org/wiki/Dvorak_keyboard_layout), which simply remaps the keycodes without any requirement for OS support. Dvorak is often touted as better-designed layout, which reduces the average travel length of the finger by better placing oft-used keys (for the English language). I recently watched [a video by Atomic Frontier entitled “Why typing sucks”](https://www.youtube.com/watch?v=188fipF-i5I), which summarises the key points quite well. It particularly finds experimentally that, if an ortholinear form factor provides a small improvement on a normal staggered QWERTY keyboard, switching to a Dvorak layout provides a whopping 26% improvement.

<div class="wp-block-image is-style-default"><figure class="aligncenter size-full is-resized">![Screenshot from https://youtu.be/188fipF-i5I?t=418 showing that an ortholinear keyboard provides a 0.3% improvement on typing comfort, while Dvorak provides a 26.2% improvement.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/Screenshot-2023-11-27-at-09.58.03.png)<figcaption class="wp-element-caption">Source: <https://youtu.be/188fipF-i5I?t=431></figcaption></figure></div>With such easy access to a Dvorak layout, I figured I should give that a go. While I didn’t do as thorough a job at evaluating progress as this video did, I however collected some statistics over time from [GTypist](https://www.gnu.org/software/gtypist/). While I now am, 15 years down the line, quite proficient with Dvorak, and use it on any keyboard form factor without any frustration, the data I collected at the time validated the frustration that I felt at the time, where I made a lot more typing mistakes during the transition period, and my typing speed noticeably dropped as a result. My typing speed now appears to be slightly better than when I abandoned the QWERTY layout. Its is also worth noting that I can switch to a QWERTY layout with only a few minutes of confusion, and only a slightly elevated error rate once I re-adjusted to it. AZERTY comes at a higher cognitive load, though. Fortunately, I don’t have to use this layout often, if at all.

<div class="wp-block-image"><figure class="aligncenter size-full is-resized">![A few relatively ugly graphs showing typing speeds and error with various keyboards and form factors over time. By 2013.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/02/image.png)<figcaption class="wp-element-caption">Qx: QWERTY; Dx: Dvorak; xT: Typematrix (2009, 2013, 2015); xM (2009, 2013), xD (2024): laptop keyboards, xE: Ergodox (2015)</figcaption></figure></div>Coming back to the Atomic Frontier video, it mentions other layouts that may have better typing comfort improvement than Dvorak ([COLEMAK](https://colemak.com/) is often mentioned in the wild). More interestingly, it also designs layouts with similar ranges of typing comfort improvement, but much fewer key location changes. I’d expect those layouts to be much faster to learn, and therefore a better target to learn over Dvorak. The only problem being that, far worse than Dvorak, OS support would be bitterly lacking, which would probably warrant custom keyboards with, like the TypeMatrix, harware-based keycode remapping. Barring those issues, it feels like it would be the best bet for wide adoption, with a concerted effort by keyboard manufacturers and/or countries, like [has happened for the recent algorithm-based update to the French layout](http://norme-azerty.fr/en/).

<div class="wp-block-image"><figure class="aligncenter is-resized">![A QWERTY keyboard with 8 key swapped to provide a 31% improvement in typing comfort (on the Bee movie) from https://youtu.be/188fipF-i5I?t=715](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/11/Screenshot-2023-11-27-at-10.03.49.png)<figcaption class="wp-element-caption">Source: <https://youtu.be/188fipF-i5I?t=714></figcaption></figure></div>Speaking of OS support, when switching to Dvorak full-time, I started running into issues where the hardware key-swap of the TypeMatrix with a `us(intl)` dead key layout did not match the native `us(dvorak-intl)`. Some of the keys and modifiers were not in the same location, which became quite frustrating. I set out to fix it in [xkeyboard-config](https://freedesktop.org/wiki/Software/XKeyboardConfig/) by making it an exact swap mapping to the `us(intl)` layout. To my delighted surprise, [my changes were accepted upstream](https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/commit/159f76d711bc8682e7e49bd6123535b35c0276bf), and have since then been available on every Unix distribution I use!

## Kinesis Advantage and Ergodox

After a few years of use, I had the unpleasant surprise of both of my TypeMatrix slowly dying on me in quick succession. I started looking around for more solid alternatives, and looked for keyboards with mechanical switches. I quickly happened upon [the venerable Kinesis Advantage](https://kinesis-ergo.com/support/advantage/). I found this keyboard to be most comfortable, and to somewhat enforce a good posture when using it, as it’s not really practical to use it when slouching. It also supports reprogramming the keys, to place them where desired. Unfortunately it lacks a few keys where I have come to expect them, particularly the middle column of `Enter` and `Backspace`.

Around that time, the [first versions of the Ergodox split keyboard](https://www.ergodox.io/) appeared, and I snaffled a DIY kit from Massdrop (now just Drop). Like the Kinesis, it is a split design, with a custom firmware, and enough keys to have my middle columns back. The default layout is quite close to a normal QWERTY, but it caused a few clashes in `us(dvorak-intl)`, such as opening/closing brackets not being in very logical positions wrt to each other. I ended up [adapting some of the layout in the firmware](https://github.com/shtrom/ergodox-firmware), so it makes more sense in Dvorak, at the cost of less sense in QWERTY.

<figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/04/Screenshot-2023-04-27-at-17.48.32-1024x441.png)</figure>I aimed for as much symmetry as possible. For example `up`/`down` are on the right thumb and `pgup`/`pgdown` are on the left, while `left`/`right` are on the right bottom row (middle/ring fingers), and `home`/`end` are in similar position on the left. I move the brackets/curlies and slashes to each side of the thumb clusters.

This is my current favourite setup, though I still have plans to add missing column keys (and a USB hub) to my Kinesis Advantage to bring it up to par. However, a setup is as bad as its worst element.

# Soft keyboards

Spending so much time on a single input device is not really useful if other related tools don’t get a look over, too. The next obvious target is a close cousin, the soft keyboard on smart phones. Surely if a wide QWERTY layout is not great for two-hand typing on a wide desk, it doesn’t make much sense at all for one-or-two thumb input on a tall screen. In this case, though, an ortholinear form factor with a Dvorak layout does not make much more sense, as it would be packing as many little keys in such a small space.

[Ploum wrote about input methods for mobile devices](https://ploum.net/writing-on-a-smartphone-review-of-8pen-and-messagease/index.html),. While my memories are blurry, I suspect I took all my recommendations from his article. I tried [8pen](https://8pen.com/) first, which was an interesting idea with the promise of being able to enter text without having to look at the screen. Unfortunately, I found it too slow to use for day-to-day entry.

<div class="wp-block-image"><figure class="alignright size-medium is-resized">![A screenshot of an Android phone running Thumb-Key](https://i0.wp.com/blog.narf.ssji.net/wp-content/uploads/sites/3/2024/03/signal-2024-03-01-000049.png?fit=135%2C300&ssl=1)</figure></div>[MessageEase](https://www.exideas.com/ME/index.php) was the next on the list, and this one stuck. It uses a 3×3 key layout, with a 1×3 space bar at the bottom and a an additional 4×1 column of control keys. This is few enough key that each is large enough to easily hit on a small screen. Like the Dvorak keyboard, it places the 9 most common keys “closer” by making them tappable, while all other keys and symbols are accessible via swipe out of each key via the sides or corners. This provides a sufficient number of combination for day-to-day entry and, unlike 8pen, it actually works fairly well for blind operation.

Sadly, MessageEase has been moribund for years and, while updates for new Android versions kept coming nothing else evolved. Recently, they moved to a subscription model, and the updated application started needing Internet access permissions, which is not something that I’m willing to give to a keyboard used to type passwords and other private information. Moreover, this made me realise that relying on proprietary software for such a crucial tool was not sustainable.

Fortunately, a [Free Software reimplementation](https://github.com/dessalines/thumb-key) exists: [Thumb-Key](https://f-droid.org/en/packages/com.dessalines.thumbkey/). I have only migrated to it a few weeks ago. It lacks a few nice-to-have features of MessageEase (complex gestures and more international typing), but has sufficiently many of the basics to be a viable replacement. I initially thought I’d teach myself the native Thumb-Key layout which is different from MessaseEase but, much like migrating from Dvorak, I gave up after a week and went back to using a MessageEase-compatible layout which is conveniently available by default.

# Mouse and arm comfort

The final piece of the puzzle is the accessory used to aim at windows and copy/paste text, the mouse. I haven’t done as much looking around on this front, but came across the [Evoluent Vertical Mouse](https://evoluent.com/products/vm4r/), which I really like. The main argument in favour of a vertical mouse is that it prevent twisting the bones of the forearms from a vertical arrangement at the elbow to a horizontal position at the wrist. Between this and the 3 additional buttons, it is convenient enough that I’m always on the lookout for more on eBay, where they occasionally show up at good prices, just so I have spares.

Another little accessory that did wonder for my wrists, while using a keyboard at a desk are [Wristease](http://wristease.com/). They are wrist-attached pad that prevent bending wrists down on the way to the keyboard. I found that the usual keyboard-attached pads for that purpose didn’t really work for me, where I suspect that the Wristease were a key factor in fixing my RSI.

# Conclusion

So this is a quick summary of my journey towards improving the quality and comfort of my input device. My initial motivation was preventing my arm RSI from getting worse. Between Wristease, an ortholinear keyboard with a Dvorak layout (with proper hand alternation), and a vertical mouse (in order of suspected importance), it has been completely fixed.

I spent a lot of time on physical keyboards, but I think mobile soft-keyboards also benefit from an independently designed input method that doesn’t just copy desktop accessories.

As an added bonus, now, no one can use my devices without struggling a lot to get anywhere. So, I guess that’s that.