---
id: 798
title: 'URL completion in dmenu'
date: '2023-02-09T23:48:45+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=798'
permalink: '/?p=798'
---

I have parted with [FVWM](http://www.fvwm.org/). Not that I was dissatisfied with more than 12 years of using it and organically growing its configuration. I was not.

But I was recently shown [i3](http://i3wm.org/) which, despite not being [Awesome](http://awesome.naquadah.org/), is indeed awesome. Particularly in the usability of its default, which I found did not require many a tweak. I was however a bit confused at first, then impressed, when I realised that the auto-generated configuration took into account my Dvorak keymap, and updated the keybindings so the keys would be the same as those on a QWERTY keyboard. That’s thoughtfullness.

The next great thing about i3 (save for `$mod+Return` to start a term anywhere, anytime), is [dmenu](http://tools.suckless.org/dmenu/). At a press of the relevant binding (equivalent to `$mod+d` on an 200-year-old keymap), one gets to enter a one-line entry where any command can be entered for execution, with incremental completion.

Dmenu is also nice due to its modularity. It takes a list of strings that can be completed on `stdin`, and outputs the typed or selected string on `stdout`, for consumption by whatever script called it.

I figured that it should be possible to handle URLs in a dmenu script. It is actually pretty trivial, and the friend who convinced me to take the jump also provided such a script, which would simply open the typed URL. But I wasn’t entirely satisfied, as recent years of browser usage taught me to expect URL completion. So I looked into ways of doing it.

  
As mentioned before, dmenu expects completionable strings to be piped into its `stdin`, so all we need to do is extract the history from the browser.

I use Firefox, which stores history in an SQLite3 database named `places.sqlite` in the profile directory. This database contains a number of tables, but the most interesting is named `mov_places`.

```
sqlite> .schema moz_places
CREATE TABLE moz_places ( id INTEGER PRIMARY KEY, url LONGVARCHAR, title LONGVARCHAR, rev_host LONGVARCHAR, visit_count INTEGER DEFAULT 0, hidden INTEGER DEFAULT 0 NOT NULL, typed INTEGER DEFAULT 0 NOT NULL, favicon_id INTEGER, frecency INTEGER DEFAULT -1 NOT NULL, last_visit_date INTEGER , guid TEXT, foreign_count INTEGER DEFAULT 0 NOT NULL);
CREATE INDEX moz_places_faviconindex ON moz_places (favicon_id);
CREATE INDEX moz_places_hostindex ON moz_places (rev_host);
CREATE INDEX moz_places_visitcount ON moz_places (visit_count);
CREATE INDEX moz_places_frecencyindex ON moz_places (frecency);
CREATE INDEX moz_places_lastvisitdateindex ON moz_places (last_visit_date);
CREATE UNIQUE INDEX moz_places_url_uniqueindex ON moz_places (url);
CREATE UNIQUE INDEX moz_places_guid_uniqueindex ON moz_places (guid);
```

Beyond the `url`, it also has a `visit_count` field which we could use to sort the URLs by popularity. So let’s!

```
$ sqlite3 .mozilla/firefox/plzrxwjv.default/places.sqlite  "select url from moz_places reverse order by visit_count desc" | head
http://jenkins.example.com/
https://server.example.net/stats/
https://cloud.example.net/apps/calendar/
https://pocket.example.net/?view=home
https://cloud.example.net/apps/external/2
https://server.example.net/mail/
https://jenkins.example.com/job/base/
https://pocket.example.net/
https://webmail.example.com/
https://www.citeulike.com/
```

This works pretty well. The only issue is that Firefox uses random names for the profile folder. We can however assume that the vast majority of the users (a singleton of me) will only have the one profile, so shell globs should be sufficient.

Another refinement could be in the fact that we don’t really want to complete all URLs ever visited, even once. So let’s limit the list to URLs which have been visited twice.

Piping this into dmenu, and telling the browser to open the URL, with some normalisation if needed, gets us the final, complete script, `dopenurl.sh`.

```
#!/bin/sh
URL=$(sqlite3 ~/.mozilla/firefox/*.default/places.sqlite  "select url from moz_places reverse where visit_count>1 order by visit_count desc" | dmenu -p "Web:")
if [ -n "$URL" ]; then
  if echo ${URL} | grep -qvi '^https\?:'; then
          URL=http://${URL}
  fi
  xdg-open "${URL}"
  exec i3-msg [class="^Mozilla Firefox$"] focus
fi
```

At this point, all that remains is to let i3 know how to execute the script. This is done by adding the following in `~/.i3/config`, assuming the script is installed as `~/bin/dopenurl.sh`.

```
bindsym $mod+c exec --no-startup-id dopenurl.sh
<a href="http://narf.jencuthbert.com/wp-content/uploads/sites/3/2015/09/blasturvion-i3-dmenu.png"><img alt="URL completion with dmenu" class="aligncenter wp-image-166" decoding="async" height="240" loading="lazy" sizes="(max-width: 1024px) 100vw, 1024px" src="http://narf.jencuthbert.com/wp-content/uploads/sites/3/2015/09/blasturvion-i3-dmenu-1024x240.png" srcset="https://blog.narf.ssji.net/wp-content/uploads/sites/3/2015/09/blasturvion-i3-dmenu-1024x240.png 1024w, https://blog.narf.ssji.net/wp-content/uploads/sites/3/2015/09/blasturvion-i3-dmenu-300x70.png 300w, https://blog.narf.ssji.net/wp-content/uploads/sites/3/2015/09/blasturvion-i3-dmenu-768x180.png 768w, https://blog.narf.ssji.net/wp-content/uploads/sites/3/2015/09/blasturvion-i3-dmenu-1536x360.png 1536w, https://blog.narf.ssji.net/wp-content/uploads/sites/3/2015/09/blasturvion-i3-dmenu-2048x480.png 2048w" width="1024"></img></a>
```