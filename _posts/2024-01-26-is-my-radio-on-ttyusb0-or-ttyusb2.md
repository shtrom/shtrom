---
id: 1330
title: 'Is my radio on ttyUSB0, or ttyUSB2?'
date: '2024-01-26T17:38:42+11:00'
author: 'Olivier Mehani'
excerpt: "I got fed up with having to guess the name of my ttyUSB radio devices, so I wrote a udev rule to create symlinks automatically.\n\nA file containing the following can go in, say, /etc/udev/rules.d/99-usb-radios.rules:\n```SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"1a86\", ATTRS{idProduct}==\"7523\", SYMLINK+=\"radio-ubitx\"```"
layout: post
guid: 'https://blog.narf.ssji.net/?p=1330'
permalink: /2024/01/26/is-my-radio-on-ttyusb0-or-ttyusb2/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '1'
image: /wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-05-12.png
categories:
    - ham
    - sysadmin
    - tip
tags:
    - Linux
    - udev
---

When connecting Ham radios to a computer, one quickly gets overwhelmed with the number of `ttyUSB*` devices created. The devices get assigned a mystically variable number depending on boot-time detection, order of connection, position of the stars, and the last fully digested meal of the pet whose most recent birthday it is.

I finally got fed up with this issue the other day, and wrote a udev rule to create symlinks automatically. For each known device. A file containing the following sort of incantations can go in, say, `/etc/udev/rules.d/99-usb-radios.rules`

```
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="radio-ubitx"
```

<figure class="wp-block-image size-full">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-26-16-05-12.png)</figure>The rules can be reloaded without a reboot with:

```
sudo udevadm control -R
```

I also learnt of a [convenient way to find all the attributes of a device](https://inegm.medium.com/persistent-names-for-usb-serial-devices-in-linux-dev-ttyusbx-dev-custom-name-fd49b5db9af1#a21f).

```
udevadm info /dev/ttyUSB0 --attribute-walk
```