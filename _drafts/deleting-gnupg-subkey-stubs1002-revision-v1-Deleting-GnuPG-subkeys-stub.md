---
id: 1005
title: 'Deleting GnuPG subkeys stub'
date: '2023-10-03T16:56:37+11:00'
author: 'Olivier Mehani'
excerpt: 'GnuPG sometimes gets confused about which smartcard a subkey is on, and refuses to use it from the currently-available card. Here''s a quick script to fix the issue.'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1005'
permalink: '/?p=1005'
---

GnuPG sometimes gets confused about which SmartCard a subkey is on, and refuses to use it from the currently-available card.

tl;dr: Here’s a quick script to fix the issue.

```
$ export SUBKEYID=...
$ KEYGRIP=$(gpg --with-keygrip -k ${SUBKEYID} | sed -n "/${SUBKEYID}/,/$/{s/ *Keygrip = //p}" )
$ rm -i ~/.gnupg/private-keys-v1.d/${KEYGRIP}.key
$ gpg --card-status  # recreate the stub from the daily-use key
```

When using an OpenPGP SmartCard, or other tokens that can be used by GnuPG, the secret key remains on the card, and never leaves. Locally, GnuPG creates a *stub*, which tells it which card to look for when the key is needed.

I had to rotate some expired subkeys today, so I loaded my master key from its dedicated card. Doing so, my local GnuPG installation updated the stub of my encryption subkey. Once all rotations were all well and done, `gpg` stubbornly contitued trying to access the subkey from my master card. This led to the classic error message

```
gpg: encrypted with 2048-bit RSA key, ID 0x..., created YYYY-MM-DD
"User Name uname@example.net"
gpg: public key decryption failed: Operation cancelled
gpg: decryption failed: No secret key
```

Based on [information from this thread](https://gnupg-users.gnupg.narkive.com/gSBmiYJu/deleting-a-smart-card-secret-key-stub-from-the-secret-keyring), I came up with the handy little script above to do the deed. It could easily be made into a one-liner, but it would have been a bit detrimental for readability, so I abstained in this instance.