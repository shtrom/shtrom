---
id: 284
title: 'Mitel 5212 phone as SIP client for a FRITZ!Box 7390'
date: '2017-08-10T22:59:30+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=284'
permalink: /2017/08/10/mitel-5212-sip-client-fritzbox-7390/
iawp_total_views:
    - '22'
categories:
    - hardware
    - sysadmin
tags:
    - DHCP
    - FRITZ!Box
    - Mitel
    - PXE
    - SIP
---

Until last year, work had [Mitel 5212 softphones](http://edocs.mitel.com/UG/EN/2ICP_5212_5224_UG_R3.pdf) as the main devices on desks. This was the case since 2008, and was apparently high time to replace them. As they had nowhere to go but the bin, I grabbed a few in the hope to use them at home. While Mitel has a proprietary protocol (MiNET), they also support standard SIP through another vendor firmware, which allowed me to add a few more physical phones behind my FRITZ!Box.

## Initial setup

The phones run off of PoE. While I initially tried to build a dumb PoE injector, I ultimately decided to buy a PoE switch instead.

Once the phone boot, they will send DHCP requests, and try to connect to a MiNET server. The first thing to do is to change the phone mode to SIP. I’m writing this retrospectively, but it seems that[ pressing `*` and `7` while the phone boots would give access to the menu allowing to change that mode](https://www.voip-info.org/wiki/view/Mitel+MiNET+to+SIP+Conversion).

It will then be necessary to load the SIP firmware. This requires a TFTP server. While a DHCP server can be configured to send all the necessary options for the phone to contact the TFTP server, I found it easier to just configure this in the phone. Rebooting it and pressing either the `Up` or `Down` arrow will lead to a menu allowing to set the TFTP server address (`Configure Phone > Network Settings > TFTP Svr Address`).

Mitel used to offer SIP firmwares at <http://sipdnld.mitel.com/>, but this site is now down. Fortunately, some copies are still floating around. I use the [one suggested from this site](https://www.voip-info.org/wiki/view/Mitel+SIP+Firmware), `Mitel_SIPphones_8.0.0.4.zip` (MD5: 8943249ffa11c175e2c56ff5171cda9a, SHA156:4e2a22e7caf4b07eb23ebc7ff4a10a1d3ffd01422e65d659447c112b93a25517), worked for me (note that, according to [this page](https://www.voip-info.org/wiki/view/Mitel+SIP+Firmware), at least version 7.2 needs to be installed on the phone prior to flashing; fortunately, this was my case). It actually contains more than support for the 5212; here is a list of SIP firmwares available in that archive.

- sip3000
- sip5212
- sip5215
- sip5220
- sip5224
- sip5235
- sipNavd (Navigator)

To serve these files to the phone over TFTP, I set up DNSMASQ to provide both a TFTP server, and a DHCP proxy offering PXE options (but no IP addresses, as this is the router’s job). Beyond upgrading the phones, this allows to [boot other machines on the network, but that is a different story](https://blog.narf.ssji.net/2013/06/pxelinux_openbsd_install/). This can simply be set up with the following options.

```
dhcp-range=192.168.1.0,proxy
dhcp-boot=pxelinux.0,192.168.1.2 # The IP address of this server (for TFTP)
pxe-service=x86PC,"Automatic Network boot",pxelinux

enable-tftp
tftp-root=/srv/tftproot

# Disable DNS
port=0
```

As I used the Debian package, I simply put those in `/etc/dnsmasq.d/pxe-proxy.conf` and restarted the service. The firmware archive must be extracted at the root of the `tftp-root`; I only extracted `Sip5212Dpl_00.bin`, for obvious reasons.

At this stage, the phone should be able to boot and load the SIP firmware, then reboot in SIP mode.

## FRITZ!Box config

The next step is to create a SIP account for the phone, and map it to incoming/outgoing lines (which can also be from an upstream SIP provider).

It’s just a matter of adding a new telephony device (*Telephony/Telephony Devices/Configure New Device*), then follow the prompts to make it a telephone, configure outgoing and incoming numbers, and create the SIP account.

[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-24-22-04-56-220x300.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-24-22-04-56.png)[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-24-22-05-34-220x300.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-24-22-05-34.png)[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/08/Screenshot-from-2017-07-24-22-07-44-217x300.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/08/Screenshot-from-2017-07-24-22-07-44.png)

##  [![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/08/Screenshot-from-2017-07-24-22-06-39-220x300.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/08/Screenshot-from-2017-07-24-22-06-39.png)

## Mitel 5212 Configuration

The freshly-created SIP account can now be configured into the Mitel phone. It has a web admin interface on port 80. The default credentials are `admin`/modelnumber (`5212`, in this case). The quick start page contains all the necessary settings: user name and SIP server address.

<figure class="wp-caption thumbnail aligncenter" id="attachment_309" style="width: 300px;">[![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-30-21-45-41-300x225.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2017/07/Screenshot-from-2017-07-30-21-45-41.png) <figcaption class="wp-caption-text">Configuring Mitel 5212 to use a FRITZ!Box SIP server</figcaption></figure>There are a number of other useful options available in the rest of the web interface, but just those are sufficient to get the phone going. Particularly, I found I didn’t have to touch the dialplan in either the FRITZ!Box or the phone.

That said, I also found that, to dial number comfortably, some dialplan rules could be added (*Dial Plan* on the left menu), to allow dialling without having to press an additional dial key, but also support numbers of various length, as well internal ones (which start with two stars, while the phone will only accept one). I set the following options.

- *Auto Dial* to *On*
- An inter-digit timeout of *3 seconds*
- Just add a `*` prefix before sending the number to the FRITZ!Box for dialled digits `*x.T` (star, followed by a single number and a timeout; quick dials)
- The same for dialled digits `*xxx.T` (star, followed by three numbers and a timeout; other devices)

## Weather

As an added bonus, the Mitel phone can display RSS feeds, but is picky on the form, and can only show the title of each entry. As it has a pre-built weather option, I decided to fill that one in with the relevant RSS feed. The [PHP code for that is available here](https://scm.narf.ssji.net/git/weather.rss/), based on data from [WebCal.fi](http://www.webcal.fi/).

## tel: protocol handler

(Edit 2020-11-03). I realised I could further the integration and have nearby phones conveniently ring when I click a link on a computer. I wrote a quick one-page [PHP protocol handler for the `tel:` scheme](https://gist.github.com/shtrom/6e1e0a1981741a23aa86488ea816b77c "https://gist.github.com/shtrom/6e1e0a1981741a23aa86488ea816b77c"), with selectable phone devices (either a Mitel phone, or the FRITZ!Box’s).