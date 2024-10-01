---
id: 679
title: 'Regaining control of a ROMMON talking at the wrong baud rate'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=679'
permalink: '/?p=679'
---

- Cisco WS-3650e-24PD
- ROMMON https://www.cisco.com/en/US/docs/routers/access/800/850/software/configuration/guide/rommon.html
- upload firmware https://community.cisco.com/t5/networking-blogs/loading-an-ios-on-a-switch-via-xmodem/ba-p/3103557: copy xmodem: flash:c3550-ipservicesk9-mz.122-44.SE6.bin)
- too slow
- set BAUD 115200 didn’t work (minicom)
- set BAUD 28800 (no support: bung, no FTDI)
- arduino SoftwareSerial https://www.arduino.cc/en/Reference/SoftwareSerial
- max232: https://www.ti.com/lit/ds/symlink/max232.pdf
- bread board https://www.arduino.cc/en/Tutorial/ArduinoSoftwareRS232

- Remote CVE in SmartInstall https://nvd.nist.gov/vuln/detail/CVE-2018-0171 https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20180328-smi2 `no vstack`

<figure class="wp-block-image size-large">[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2019/11/IMG_20191106_231056.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2019/11/IMG_20191106_231056.jpg)</figure><figure class="wp-block-image size-large">[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2019/11/IMG_20191106_231137.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2019/11/IMG_20191106_231137.jpg)</figure>