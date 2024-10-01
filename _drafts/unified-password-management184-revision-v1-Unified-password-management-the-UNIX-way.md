---
id: 1550
title: 'Unified password management, the UNIX way'
date: '2024-05-09T13:08:14+10:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1550'
permalink: '/?p=1550'
---

I’ve long been meaning to store all my passwords in a single, safe, location, as a [way to remain sane as well as safe](https://www.schneier.com/blog/archives/2014/09/security_of_pas.html). But which one? Every operating system (or desktop environment) now has its own store, but choosing one casts a lot of things into stone, and most have a lot of third-party dependencies.

[KeePass](https://www.keepassx.org/) seems to be a good cross-platform solution, with clients for [Linux, Windows, OS X](https://www.keepassx.org/downloads/) and even [Android](https://f-droid.org/repository/browse/?fdfilter=keepassx&fdid=com.android.keepass), and nice features such as filling on demand. But I don’t like the whole clicky interface, if only for use without graphical display. It also doesn’t offer a native way to synchronise the stores across boxes.

For a while, I have been storing all my important configuration files in a git repository, with some make magic to install and update the files on the system. This magic would also store all passwords in a GPG-encrypted files, and replace them when installing the files.

The problem, of course, is that the passwords are still in plaintext in the live systems. And it came back to bite me when I sent an innocuous script (the `ics2dav.sh` script from [this post](https://blog.narf.ssji.net/2015/03/caldav-tools-for-the-console/)) to a friend… with the password nicely sitting there. Fortunately, I noticed this before him, and changed my password. In addition, this doesn’t cater for passwords stored in other applications, such as Firefox.

So things had to change. And I discovered [pass](http://www.passwordstore.org/)[(1)](http://linux.die.net/man/1/pass), a simple command-line tool based on GPG-encrypted flat files, with an option to sync natively with Git. So there is finally an option for me to store passwords in a way which fits my workflow.

# Getting the password store going

The password store itself is easy to get going with, as documented on [its website’s frontpage](http://www.passwordstore.org/). Once initialised (with `pass init`), some juggling of `pass add ENTRY` (or `pass generate ENTRY`) and `pass ENTRY` are sufficient to interact with the store. There is also a `-c` option to copy the password to the clipboard for some time, without displaying it.

I initially chose a two-levels free-text structure, to group passwords by relationship (e.g., one set of personal domains, or work-related passwords). However, gradually importing other passwords proved this to not be flexible enough. I settled for a loose structure of the form `CATEGORY/DOMAIN/USERNAME`. If I only have one username for a domain, I simply list it in the following lines of the password file, as `login: USERNAME`, along with other useful information. For example, `test/example.net` would look as follows.

```
PASSWORD
login: USERNAME
url: *example.net/*
email: shtrom+example@ssji.net
secret question: what is your favourite colour? / Blue... No! Red!
```

# Integrating the store in other applications

The rest of the challenge is now to integrate the password store in the rest of my workflow. Some are easy, some need helpers, some need addons, and some need patches.

## Shell scripts

Shell scripts are the easiest to integrate pass in. A simple backticked `pass ENTRY` instead of the verbatim password does the trick.

## Email

I use [OfflineImap](http://offlineimap.org/) to sync my emails from remote IMAP servers to a local store. It’s configuration file is a Pythonish script, which allows the [inclusion of a helper file](http://offlineimap.org/), where functions can be defined. For this purpose, I defined a `get_pass` function.

The main configuration file looks as follows.

```
[general] 
accounts = Example
pythonfile = ~/.offlineimap.py

[Account Example]
localrepository = ExampleLocal
remoterepository = Example

[Repository Example]
type = IMAP
remotehost = mail.example.net
remoteuser = USERNAME
remotepasseval = get_pass("test/example.net")

[Repository ExampleLocal]
type = Maildir
sep = /
localfolders = ~/Mail
```

The `.offlineimap.py `is pretty simple. I didn’t write it myself, but cannot recall its origin…

```
#! /usr/bin/env python
from subprocess import check_output

def get_pass(account):
 return check_output("pass %s | head -n 1" % (account), shell=True).rstrip().decode("utf-8")

if __name__ == "__main__":
 import sys
 print(get_pass(sys.argv[1]))
```

Note the attention to details: if called on its own, the script will just output the requested password (rather than the multi-line contents) on stdout.

Sending email, with [sSMTP](http://packages.qa.debian.org/s/ssmtp.html), can be done in a similar way with a wrapper shell script.

```
#!/bin/bash
#mailhub=smtp.example.net # XXX This could be stored in the password store too.
#rewriteDomain=example.net
USERNAME="USERNAME"
PASSWORD=`pass test/example.net | head -n 1`
/usr/sbin/ssmtp -au ${USERNAME} -ap ${PASSWORD} $*
```

I haven’t tried this one thoroughly, as I generally use smart-hosts allowing relay based on network origin.

## CalDAV sync

I described, [in a previous post](https://blog.narf.ssji.net/2015/03/caldav-tools-for-the-console/), my use of a number of tools to hit my [ownCloud](https://owncloud.org/)‘s DAV shares and sync calendar and contact lists. I use [vdirsyncer](https://vdirsyncer.readthedocs.org/) for this purpose.

Its configuration syntax has changed a bit recently, but my current `.vdirsyncer/config` configuration file contains the following instead of the `password` field.

```
password.fetch = ["command", "~/bin/vdirsyncer_password_command.sh", "USERNAME", "example"]
```

The `vdirsyncer_password_command.sh `is once again a trivial exercise in reordering arguments and passing them to another binary, with some logic to map well-know server names to categories.

```
#!/bin/sh
# usage: vdirsyncer_password_command.sh USERNAME SERVER
USERNAME=$1
SERVER=$2
ACCOUNT=$SERVER

if echo ${SERVER} | grep -q 'example.\(net\|org\)'; then
 ACCOUNT=example

fi
pass ${ACCOUNT}/${USERNAME} | head -n 1
```

## Firefox

All the above served me well for a while, but the elephant in the room was a panda. That is, until I realised there is a handy [extension for Firefox, PassFF, which integrates with the password store](https://addons.mozilla.org/en-US/firefox/addon/passff/).

The remaining problem was to export all those passwords that I already had stored in Firefox. Fortunately, [another extension allows to export all your password as an XML or CSV file](https://addons.mozilla.org/en-US/firefox/addon/password-exporter/).

Some [sed(1)](http://linux.die.net/man/1/sed) magic later, I had a script which would insert all those passwords into the store, keeping `username` and `url` information as described above. This allows the extension to better match credentials to sites.

```
$ sed -n 's/.*host="https\?\(www\.\)\?:\/\/\([^"]\+\)".*user="\([^"]\+\)".*password="\([^"]\+\)".*/pass add -m firefox\/\2 << EOF\n\4\nlogin: \3\nurl: *\2/*\nEOF/p' password-export-YYYY-MM-DD > password.sh
$ bash password.sh
```

## Android

The next objective, now that my computers all have a nice distributed synced password store, is to also allow its use with my Android device. Once again, “there’s an app for that”, [Password Store](https://f-droid.org/repository/browse/?fdid=com.zeapo.pwdstore). It integrates with [OpenKeyChain](https://f-droid.org/repository/browse/?fdid=org.sufficientlysecure.keychain) to do the GPG decryption.

Nonetheless, this is a mobile device, easily stolen or forgotten, so I am reluctant to store my private encryption key on it. As a matter of fact, I am also reluctant to do this on normal machines, but [I use an OpenPGP smart card to store it instead](https://www.narf.ssji.net/~shtrom/wiki/tips/openpgpsmartcard) (along with my SSH key).

There is obviously no smart card reader on my phone, but it fortunately supports NFC, so I am using a [YubiKey Neo](https://www.yubico.com/products/yubikey-hardware/yubikey-neo/). It works nicely, [both on a desktop computer and Android device](https://www.narf.ssji.net/~shtrom/wiki/tips/openpgpsmartcard?&#yubikey_neo). Unfortunately, it doesn’t seem to be currently possible to use the Authentication key for SSH authentication to push/pull changes to the password store, but [there is an issue open about it](https://github.com/zeapo/Android-Password-Store/issues/71).

## Gajim

I have used [Gajim](_wp_link_placeholder) as my Jabber client for pretty much ever. This is one outstanding application where there is no way to provide a wrapper to fetch the password. I wrote an [initial support for pass(1), and opened an issue](https://trac.gajim.org/ticket/8217). Hopefully, full support will become available upstream soon, but I’ll probably have to rework the patch.

## ownCloud

The ownCloud desktop client keeps asking for a password. This is annoying, and I’ll have to look into it.

## Conclusion

I now have about 300 passwords (after cleanup) that I don’t need to remember anymore, and are all safely locked away in GPG-encrypted files, except for when I need them. Yay!

A quick [grep(1)](http://linux.die.net/man/1/grep) still shows one recalcitrant password still hard-coded in my git repository, in a Perlish configuration file that I need to eliminate when I’m back in the right network to test. I think, however, that backticks will do the trick.

It would also be nice to have a bridge to other stores or protocol such as GnomeKeyring, so not all applications need native support or patches to be able to use this, as I did for Gajim.

## Updates

- 2016-01-19: Added stubs on YubiKey Neo and ownCloud.
- 2016-02-23: Added a missing `head -n 1` in the sSMTP script, which is necessary in case of multi-line files