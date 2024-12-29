---
id: 1731
title: 'Remap thumb buttons on the Evoluent Vertical Mouse (MV4R)'
date: '2024-12-09T18:04:11+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1731'
permalink: '/?p=1731'
---

```
```
# remap the thumb button of the Evoluent MV4R to the Activities view in GNOME
# (Super key)
evdev:name:Evoluent VerticalMouse 4:*
 ID_INPUT_KEY=1
 ID_INPUT_KEYBOARD=1
 KEYBOARD_KEY_90004=leftshift
 KEYBOARD_KEY_90006=leftmeta
# sudo cp 70-evoluent-thumb-activity.hwdb /etc/udev/hwdb.d
# sudo systemd-hwdb update
# sudo udevadm trigger
# udevadm info /dev/input/event24
# sudo libinput debug-events --device /dev/input/event22
# sudo evtest
```

<https://discussion.fedoraproject.org/t/how-to-remap-mouse-buttons-on-gnome-with-wayland-without-running-an-extra-service/89700/5>

[https://unix.stackexchange.com/questions/326373/configure-extra-mouse-button-as-a-second-middle-click-under-wayland#comment651936\_326373](https://unix.stackexchange.com/questions/326373/configure-extra-mouse-button-as-a-second-middle-click-under-wayland#comment651936_326373)

<https://unix.stackexchange.com/questions/422470/how-to-set-device-specific-mouse-settings-in-wayland-under-libinput-debian-gnom>

```
[17:32:24] ~/bordel/default-env$ udevadm info /dev/input/event22                                  13s 130 ↵    master <br></br>P: /devices/pci0000:00/0000:00:14.0/usb3/3-4/3-4.2/3-4.2.3/3-4.2.3.1/3-4.2.3.1:1.0/0003:1A7C:0191.0027/input/input68/e><br></br>M: event22<br></br>R: 22<br></br>U: input<br></br>D: c 13:86<br></br>N: input/event22<br></br>L: 0<br></br>S: input/by-path/pci-0000:00:14.0-usb-0:4.2.3.1:1.0-event-mouse<br></br>S: input/by-id/usb-1a7c_Evoluent_VerticalMouse_4-event-mouse<br></br>S: input/by-path/pci-0000:00:14.0-usbv2-0:4.2.3.1:1.0-event-mouse<br></br>E: DEVPATH=/devices/pci0000:00/0000:00:14.0/usb3/3-4/3-4.2/3-4.2.3/3-4.2.3.1/3-4.2.3.1:1.0/0003:1A7C:0191.0027/input/i><br></br>E: DEVNAME=/dev/input/event22<br></br>E: MAJOR=13<br></br>E: MINOR=86<br></br>E: SUBSYSTEM=input<br></br>E: USEC_INITIALIZED=64666986962<br></br>E: ID_INPUT_KEYBEARD=1<br></br>E: KEYBOARD_KEY_90004=leftshift<br></br>E: KEYBOARD_KEY_90006=leftmeta<br></br>E: ID_INPUT=1<br></br>E: ID_INPUT_MOUSE=1<br></br>E: ID_INPUT_KEY=1<br></br>E: ID_BUS=usb<br></br>E: ID_MODEL=Evoluent_VerticalMouse_4<br></br>E: ID_MODEL_ENC=Evoluent\x20VerticalMouse\x204<br></br>E: ID_MODEL_ID=0191<br></br>E: ID_SERIAL=1a7c_Evoluent_VerticalMouse_4<br></br>E: ID_VENDOR=1a7c<br></br>E: ID_VENDOR_ENC=1a7c<br></br>E: ID_VENDOR_ID=1a7c<br></br>E: ID_REVISION=0001<br></br>E: ID_TYPE=hid<br></br>E: ID_USB_MODEL=Evoluent_VerticalMouse_4<br></br>E: ID_USB_MODEL_ENC=Evoluent\x20VerticalMouse\x204<br></br>E: ID_USB_MODEL_ID=0191<br></br>E: ID_USB_SERIAL=1a7c_Evoluent_VerticalMouse_4<br></br>E: ID_USB_VENDOR=1a7c<br></br>E: ID_USB_VENDOR_ENC=1a7c<br></br>E: ID_USB_VENDOR_ID=1a7c<br></br>E: ID_USB_REVISION=0001<br></br>E: ID_USB_TYPE=hid<br></br>E: ID_USB_INTERFACES=:030102:<br></br>E: ID_USB_INTERFACE_NUM=00<br></br>E: ID_USB_DRIVER=usbhid<br></br>E: ID_PATH_WITH_USB_REVISION=pci-0000:00:14.0-usbv2-0:4.2.3.1:1.0<br></br>E: ID_PATH=pci-0000:00:14.0-usb-0:4.2.3.1:1.0<br></br>E: ID_PATH_TAG=pci-0000_00_14_0-usb-0_4_2_3_1_1_0<br></br>E: LIBINPUT_DEVICE_GROUP=3/1a7c/191:usb-0000:00:14.0-4.2.3<br></br>E: DEVLINKS=/dev/input/by-path/pci-0000:00:14.0-usb-0:4.2.3.1:1.0-event-mouse /dev/input/by-id/usb-1a7c_Evoluent_Verti><br></br>E: TAGS=:power-switch:<br></br>E: CURRENT_TAGS=:power-switch:
```