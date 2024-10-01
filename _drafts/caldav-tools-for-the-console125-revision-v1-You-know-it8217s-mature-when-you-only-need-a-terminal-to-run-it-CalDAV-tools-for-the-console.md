---
id: 801
title: 'You know it&#8217;s mature when you only need a terminal to run it (CalDAV tools for the console)'
date: '2023-02-09T23:48:45+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=801'
permalink: '/?p=801'
---

*The following was [initially posted on Pump.io](https://1realtime.net/shtrom/image/PYjFmjQ_S-qaqTF44ksanA), before I realised that this might benefit from a more preservable/visible format.*

Frustrated with only interacting with my ownCloud calendar through the native web interface, I finally decided to look for a replacement application that I could run locally. [Khal](http://lostpackets.de/khal/index.html) ended up being it, with [vdirsyncer](https://github.com/untitaker/vdirsyncer) for two-way CalDAV sync with ownCloud.

Coupled with [watdo](https://github.com/untitaker/watdo), by [the same author as vdirsyncer](https://unterwaditzer.net/), for [todo.txt](http://todotxt.com/)-like management of CalDAV tasks (`VTODO`), I can now do all my schedule and tasks management from the comfort of my own terminal, even without any connectivity!

## Configuring Khal and vdirsyncer

```
$ cat .khal/khal.conf
[calendars]

[[home]]
path = ~/.calendars/home/
color = dark blue

[[work]]
path = ~/.calendars/work/
color = dark green
```

```
$ cat .vdirsyncer/config
[general]
status_path = ~/.vdirsyncer/status/

[pair contacts]
a = contactslocal
b = contacts_remote
collections = ["from b"]
[storage contactslocal]
type = filesystem
path = ~/.contacts/
fileext = .vcf
[storage contacts_remote]
type = carddav
url = http://OWNCLOUD/remote.php/carddav/
username = USERNAME
password = PASSWORD

[pair calendar]
a = calendarlocal
b = calendar_remote
collections = ["from b"]
[storage calendarlocal]
type = filesystem
path = ~/.calendars/
fileext = .ics
[storage calendar_remote]
type = caldav
url = https://OWNCLOUD/remote.php/caldav/calendars/USERNAME/
username = USERNAME
password = PASSWORD
```

Note the `collections = ["from b"]` in vdirsyncer’s config section for the `calendar` pair just gets all the calendars from ownCloud, including the `contact_birthdays` one.

[![khal](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2015/03/khal-300x168.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2015/03/khal.png)I find the parallel with [Mutt](http://www.mutt.org/)/[OfflineIMAP](http://offlineimap.org/) quite satisfying .

Vdirsyncer also syncs CardDAV entries, but I’m not sure what to do with them yet, as lbdb and pcquery (from [pyCardDAV](http://lostpackets.de/pycarddav/), from [the author of Khal](http://lostpackets.de/), fancy that!) do the job well from within Mutt.

```
$ grep pcquery -/.muttrc
set query_command="lbdbq '%s'; pcquery -m '%s' | sed 1d"
```

## Todo management with watdo

This gets even better. [ownCloud tasks](https://apps.owncloud.com/content/show.php/Tasks+Enhanced?content=164356) can add `VTODO`s, and store them in the same CalDAV backend (at the time of this writing, oC 8 needs code from Git master). `VTODO`s naturally get synced by vdirsyncer along with the rest of the calendar entries, and can then be managed locally by watdo, which summarises them in a todo.txt format in your favourite `$EDITOR`.

```
$ cat .watdo/config 
[watdo]
path = ~/.calendars/
```

Now, [my last wish on this matter is that GTG support an ICS or CalDAV backend](https://github.com/getting-things-gnome/gtg/issues/96).

## Side bonus: PUT a local ICS file into the CalDAV server

I still need to find a way to pust ICS files I receive as attachment to emails into ownCloud. I suspect the basic idea is to wrap the following into a script (perhaps using the object’s `UID `as a more unique name on the server side.

```
curl -T ~/bdata.ics -u USERNAME https://OWNCLOUD/remote.php/caldav/calendars/USERNAME/work/bdata.ics
```

### Edit: `ics2dav.sh`

```
#!/bin/sh
# A simple tool to add a flat ICal file to a remote CalDAV server
# Copyright (C) 2015 Olivier Mehani <shtrom@ssji.net>
# 
# usage:
# ics2dav.sh FILE.ics
# cat FILE.ics | ics2dav.sh
# 
# handy in Mutt:
# macro attach \ec "<pipe-entry>ics2dav.sh\n" "PUT ICal file into calendar"
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
USERNAME=YOURUSERHERE
PASSWORD=YOURPASSHERE
CALDAVURL=https://OWNCLOUD/remote.php/caldav/calendars/$USERNAME
CALENDAR=YOURCALENDARDERE

if [[ -z "$1" ]]; then
 ICSNAME=`mktemp`
 cat > $ICSNAME
else
 ICSNAME=$1
fi

OBJUID=`sed -n s/^UID://p $ICSNAME`
curl -T $ICSNAME -u $USERNAME:$PASSWORD $CALDAVURL/$CALENDAR/$OBJUID@`hostname -f`.ics

if [[ -z "$1" ]]; then
 rm $ICSNAME
fi
```

## Afterthought

What would really make me completely happy is if the [Hamster time tracker](https://projecthamster.wordpress.com/) could use or sync with `VJOURNAL` entries (stored locally, of course!).

## Update (2015-12-26)

Watdo is now deprecated in favour of [todoman](https://github.com/hobarrera/todoman).

## Updates (2016-05-16)

- Pycard is [now deprecated](https://github.com/geier/pycarddav/issues/92) in favour of vdirsyncer for the sync, and [khard](https://github.com/scheibler/khard/) for the management.
- khal has a handy [mutt2khal helper to import events straight from mutt](https://github.com/pimutils/khal/blob/master/misc/mutt2khal).