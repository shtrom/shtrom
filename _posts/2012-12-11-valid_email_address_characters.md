---
id: 17
title: '+ is a valid character in an email address!'
date: '2012-12-11T00:00:00+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://narf.jencuthbert.com/2012/12/11/valid_email_address_characters/'
permalink: /2012/12/11/valid_email_address_characters/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '2'
categories:
    - rant
tags:
    - email
    - RFC
    - standard
---

I like my mailbox organised. And I like things to be automated. Fortunately, email systems support aliases for their users, so more than one email address reaches the same person. This allows for automatic filtering depending on which address the message was sent to.

What’s even better is that these systems can match a pattern to make generic aliases (*e.g.*, <tt>user-REPLACEME@example.net</tt> for user <tt>user@example.net</tt>). This way, you can create valid email addresses on the fly, without having to tinker with anything (*e.g.*, <tt>user-gascompany@example.net</tt> for the gas company to contact the user).

Now, dash (<tt>-</tt>) is not the most common character used for that purpose. The plus character (<tt>+</tt>) is more commonly seen. Notably, but not alone, GMail supports it. If you have an account there, try sending an email to <tt>YOURUSERNAME+test@gmail.com</tt>.

And this is where my problem is. Once again, I was happily filling in a form requesting my email address, put in an address with a <tt>+</tt> in it, and got it rejected because it “contain\[ed\] invalid characters.” It really annoys me that some people who call themselves professionals in IT-related fields do not seem to be able to understand a standard properly, if they have been looking for it, at least…

Because there *is* a standard describing exactly what characters are valid in an email address. This is [RFC 5322](https://tools.ietf.org/html/rfc5322), the latest current standard for *Internet Message Format*. Amongst other things, it describes the format of an email address. This is on [page 17](https://tools.ietf.org/html/rfc5322#page-17) onwards. Granted, this is not the easiest to read, so let me single out the relevant parts.

```
addr-spec       =   local-part "@" domain
local-part      =   dot-atom / quoted-string / obs-local-part
```

The <tt>dot-atom</tt> is described on [page 13 of the same document](https://tools.ietf.org/html/rfc5322#page-13).

```
atext           =   ALPHA / DIGIT /    ; Printable US-ASCII
                    "!" / "#" /        ;  characters not including
                    "$" / "%" /        ;  specials.  Used for atoms.
                    "&" / "'" /
                    "*" / "+" /
                    "-" / "/" /
                    "=" / "?" /
                    "^" / "_" /
                    "`" / "{" /
                    "|" / "}" /
                    "~"
[...]
dot-atom-text   =   1*atext *("." 1*atext)
dot-atom        =   [CFWS] dot-atom-text [CFWS]
```

In summary, the local part (*i.e.*, username, usually) of a valid email address *can* contain, amongst other things, a series of at least one character(s), potentially separated by dots (<tt>dot-atom-text</tt>). Moreover, the list of characters allowed in this series (<tt>atext</tt>) *does contain <tt>+</tt>* (and other unusual but valid ones like <tt>\#</tt>, <tt>$</tt>, <tt>&amp;</tt>,<tt>?</tt> or <tt>{</tt>).

So, please people, when designing forms and verifying email addresses, make sure your verification procedure correctly matches the standards, rather than hand-waving your way around, and trying to guess what works and what doesn’t.

**Edit (2015-06-30):** I just realised that there is even an RFC describing the use of subaddress filtering: [RFC5233](https://tools.ietf.org/html/rfc5233).

**Edit (2016-10-26):** Finally, a good writeup on [the 100% correct way to validate email addresses](https://hackernoon.com/the-100-correct-way-to-validate-email-addresses-7c4818f24643) ([WebArchive link](https://web.archive.org/web/20160908112714/https://hackernoon.com/the-100-correct-way-to-validate-email-addresses-7c4818f24643?gi=90867777db1a))!