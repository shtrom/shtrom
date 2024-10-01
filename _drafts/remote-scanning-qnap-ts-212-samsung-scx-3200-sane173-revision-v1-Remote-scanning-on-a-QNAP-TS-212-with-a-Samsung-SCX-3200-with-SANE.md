---
id: 797
title: 'Remote scanning on a QNAP TS-212 with a Samsung SCX-3200 with SANE'
date: '2023-02-09T23:48:45+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=797'
permalink: '/?p=797'
---

I recently realised that the QNAP TS-212 NAS (running the latest QTS 4.2.0) can be used as a print server. No need to keep another machine on to print from anywhere!

## Remote printing is easy

Both UNICES, through [CUPS](https://www.cups.org/), and Windows, through [Samba](https://www.samba.org/), can use the printer straight-away. In the case of the Samsung SCX-3205, the driver under ArchLinux is the [samsung-unified-driver (from AUR)](https://aur.archlinux.org/packages/samsung-unified-driver) which, fortunately, doesn’t install any useless binary beyond those needed by the PPD used by CUPS.

```
client$ pacman -Qs samsung
local/samsung-unified-driver 1.00.36-2
```

## Remote scanning is harder

The problem is that this is a combo printer/scanner. Moving the printer to the NAS requires a similar solution to CUPS to scan from the network. Fortunately, [SANE](http://sane-project.org/) can do this, and there is [some documentation about setting it up on a QNAP NAS](http://forum.qnap.com/viewtopic.php?t=8351). In this case, however, this did not work smoothly, so I had to fix a few things.

SANE is available through `sane-backends` in the [Optware IPKG](http://www.nslu2-linux.org/wiki/Optware) repository (installable from the QTS *App Center*). My (some-years-old) install could detect the USB device fine.

```
ts212$ sane-find-scanner
  # sane-find-scanner will now attempt to detect your scanner. If the
  # result is different from what you expected, first make sure your
  # scanner is powered up and properly connected to your computer.

  # No SCSI scanners found. If you expected something different, make sure that
  # you have loaded a kernel SCSI driver for your SCSI adapter.

found USB scanner (vendor=0x04e8, product=0x3441) at libusb:001:008
  # Your USB scanner was (probably) detected. It may or may not be supported by
  # SANE. Try scanimage -L and read the backend's manpage.

  # Not checking for parallel port scanners.

  # Most Scanners connected to the parallel port or other proprietary ports
  # can't be detected by this program.

  # You may want to run this program as root to find all devices. Once you
  # found the scanner devices, be sure to adjust access permissions as
  # necessary.
```

However, no driver seemed to be able to use it.

```
ts212$ scanimage -L

No scanners were identified. If you were expecting something different,
check that the scanner is plugged in, turned on and detected by the
sane-find-scanner tool (if appropriate). Please read the documentation
which came with this software (README, FAQ, manpages).
```

### Driver configuration to recognise the USB device

Some reading identified that scanner to be usable with the `xerox_mfp` driver, but version 1.0.22 doesn’t have the necessary entries in `/opt/etc/sane.d/xerox_mfp.conf` to match the USB ID.

```
#Samsung SCX-3200 Series, Samsung SCX-3205W
usb 0x04e8 0x3441
```

However, adding them manually didn’t help.

### IOCTL issues in libusb-0.1

Some quick [`strace`(1)](http://linux.die.net/man/1/strace) showed USB ioctl failures when trying to use the scanner device, specifically. This led me to suspect the `libusb-0.1` package provided by Optware.

```
ts212$ ldd `which scanimage`
libsane.so.1 => /opt/lib/libsane.so.1 (0xb6f60000)
libpthread.so.0 => /lib/libpthread.so.0 (0xb6f39000)
libz.so.1 => /opt/lib/libz.so.1 (0xb6f1b000)
libdl.so.2 => /lib/libdl.so.2 (0xb6f10000)
libm.so.6 => /lib/libm.so.6 (0xb6e60000)
libieee1284.so.3 => /opt/lib/libieee1284.so.3 (0xb6e50000)
libtiff.so.3 => /opt/lib/libtiff.so.3 (0xb6df0000)
libjpeg.so.62 => /opt/lib/libjpeg.so.62 (0xb6dc8000)
libusb-0.1.so.4 => /opt/lib/libusb-0.1.so.4 (0xb6db9000)
libc.so.6 => /lib/libc.so.6 (0xb6c85000)
/lib/ld-linux.so.3 (0xb6f8a000)
```

### EABI 4 vs. 5 issues

Some more digging around and playing with [`file`(1)](http://linux.die.net/man/1/file) and [`ldd`(1)](http://linux.die.net/man/1/ldd) later, I realised that, while the NAS’s system was now using the ARM EABI version 5, the Optware packages were still using version 4, which I thought might be a problem.

```
ts212$ file /bin/busybox 
/bin/busybox: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.14, stripped
ts212$ file /opt/lib/libusb-0.1.so.4.4.4
/opt/lib/libusb-0.1.so.4.4.4: ELF 32-bit LSB shared object, ARM, EABI4 version 1 (SYSV)
```

When I installed Optware, some years ago, IPKG was configured to use the `cs05q3armel` feed, which has ARM EABI4 binaries. I don’t know if this is still the case by default. However, I noticed that the `cs08q1armel` feed does provide ARM EABI5 binaries. So I swapped the feeds over, and reinstalled all the packages (with some `ipkg list_installed` and shell magic).

```
ts212$ grep cs.*armel /opt/etc/ipkg.conf
#src cs05q3armel http://ipkg.nslu2-linux.org/feeds/optware/cs05q3armel/cross/stable
src cs08q1armel http://ipkg.nslu2-linux.org/feeds/optware/cs08q1armel/cross/stable
```

### Rebuilding libusb and sane-backends

But the problem kept happening… At this point, I went for the next easiest option, which was simply to [rebuild](http://www.nslu2-linux.org/wiki/Optware/AddAPackageToOptware) ([natively](http://www.nslu2-linux.org/wiki/Info/NativeBuildMachine)) `libusb` and `sane-backends` from the [Optware source](http://svn.nslu2-linux.org/svnroot/optware) (rev 13128). I took the opportunity to bump `sane-backends` to 1.0.25, and fix a few other things, which I pushed to a [separate Git repo](https://scm.narf.ssji.net/git/optware/commit/?h=ts212&id=cadda9c4d62389ffd24f6683b2147de78f0b8fa5).

```
ts212$ ipkg install unslung-devel
ts212$ cd optware; make cs08q1armel-target
ts212$ cd cs08q1armel; make directories toolchain libusb-ipk sane-backends-ipk
ts212$ ipkg install builds/libusb_0.1.12-2_arm.ipk
ts212$ ipkg install builds/sane-backends_1.0.25-1_arm.ipk
```

This still didn’t work…

### System vs. Optware libusb

Some hopeless poking around later, I realised that some recent versions of QTS starting shipping `libusb-1.0` and `libusb-0.1` natively.

```
ts212$ file /usr/lib/libusb-0.1.so.4.4.4
/usr/lib/libusb-0.1.so.4.4.4: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV), dynamically linked, stripped
```

So I simply move the Optware library out of the way

```
ts212# mv /opt/lib/libusb-0.1.so.4{,no}
```

scanimage therefore used the next best thing, the system `libusb-0.1` and `-1.0`.

```
ts212$ ldd `which scanimage` | grep usb
libusb-0.1.so.4 => /usr/lib/libusb-0.1.so.4 (0xb6d6c000)
libusb-1.0.so.0 => /usr/lib/libusb-1.0.so.0 (0xb6c24000)
```

This was sufficient to finally detect the scanner.

```
ts212$ scanimage -L
device `xerox_mfp:libusb:001:008' is a Samsung Samsung SCX-3200 Series multi-function peripheral
```

### Sharing the scanner

Now that local scanning works, we can go back to making the device available over the network, through SANE and Xinetd, as per [the original post](http://forum.qnap.com/viewtopic.php?t=8351).

`saned` and `xinetd` must first be configured to allow connections from the local network.

```
ts212$ tail -n 2 /opt/etc/sane.d/saned.conf
192.0.2.0/24
2001:db8::/64
ts212$ grep only_from /opt/etc/xinetd.conf 
 only_from = localhost 192.0.2.0/24 2001:db8::/64
```

The `saned-backends` package installed a xinetd configuration file, which may or may not (try and let me know!) be adjusted as follows.

```
ts212# cat /opt/etc/xinetd.d/saned
service saned
{
  port = 6566
  socket_type = stream
  server = /opt/sbin/saned
  protocol = tcp
  user = admin
  group = administrators
  wait = no
  disable = no
}
```

`xinetd` also needs the sane service/port to be registered in `/etc/services`.

```
ts212# tail -n 1 /etc/services
saned 6566/tcp # SANE network scanner daemon
```

Modifying this file directly does not, however, survive reboots. Instead, an `autorun.sh` script can be modified or created in the flash configuration partition. At the same time, a command can be added so `xinetd` is started at boot.

```
ts212# mount /dev/mtdblock5 /tmp/config/
ts212# cat >> /tmp/config/autorun.sh < EOF
echo "saned 6566/tcp # SANE network scanner daemon" >> /etc/services
/sbin/daemon_mgr xinetd start "/opt/sbin/xinetd"
EOF
```

## Client configuration for remote scanning

### SANE for Unix

For the sane client library, the IP address of the scanning server has to be added in the `/etc/sane.d/net.conf` configuration file. This is all that is needed on the client to successfully scan a document.

```
client$ tail -n 1 /etc/sane.d/net.conf
192.0.2.3
client$ scanimage > a
client$ file a
a: Netpbm image data, size = 1280 x 1734, rawbits, pixmap
```

### SaneTwain for Windows

While Windows doesn’t have direct support for scanning from a remote SANE server, the nifty [SaneTwain](http://sanetwain.ozuzo.net/) TWAIN driver provides just what’s needed to do so.

## Summary

Despite going through the trouble of switching IPKG feed and rebuilding some packages, it seems the root cause of the problem was some incompatibilities between the system’s and Optware’s `libusb`, perhaps in addition to ABI issues. However, a quick test with `sane-backends-1.0.22`, which still didn’t work after everything was fixed, so perhaps `sane-backends-1.0.25` is indeed needed.