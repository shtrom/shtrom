---
id: 806
title: 'Migrating to WordPress'
date: '2023-02-09T23:49:06+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=806'
permalink: '/?p=806'
---

After a lot of humming, I decided that it wasn’t very practical to use a different platform for every blog I was running on the same machine. Some more puffing led me to conclude that WordPress was the best candidate to replace the likes of [SimplePHPBlog](http://sourceforge.net/projects/sphpblog/) and [Blogsum](http://obfuscurity.com/Tags/Blogsum). I still have an odd [Nanoblogger](http://nanoblogger.sourceforge.net/) to migrate, but it is easily maintained and keeps to itself for the moment.

In the process, I had to find ways to import data from the old platforms, and massage it into something that WordPress can work with.

# From SimplePHPBlog

There is a mention of a [SimplePHPBlog import script in the WordPress support section ](https://wordpress.org/support/topic/simplephpblog-import-utility)but the link is dead. A bit more searching [reveals a working link on another site](http://www.onestepcloser.co.nz/wordpress/?p=11).

Unfortunately, that script was written for older versions of both SimplePHPBlog and WordPress, and does not support features such as GZipped data for the latter, and some of the former’s more recent database structure. I quickly patched the script to implement this, and was left with [a working script to import SimplePHPBlog-0.5.0.1 data into WordPress-3.8.1](https://scm.narf.ssji.net/git/scripts/tree/WordPressImport.pl). I’m afraid I have broken category/tag import in the process, (Perl is really not my favourite language), but it was easily fixed manually afterwards in my case.

What’s left to do is to remap old URLs to the WordPress’s permalink. Some SQL coupled with <tt>sed</tt> voodoo can generate redirection rules for Apache nicely.

```
$ mysql --silent  -e  "select post_date, post_name from wp_2_posts;" blog | sed "/autosave/d;/revision/d;/^2014/d;s^20\([0-9]\{2\}\)-\([0-9]\{2\}\)-\([0-9]\{2\}\) \([0-9]\{2\}\):\([0-9]\{2\}\):\([0-9]\{2\}\)        \(.*\)^RedirectMatch permanent .*\1\2\3-\4\5\6.* /20\1/\2/\7^"
RedirectMatch permanent .*081118-210006.* /2008/11/letter-to-nestle-re-hot-drink-machine-at-orange-airport
[...]
RedirectMatch permanent .*130702-143711.* /2013/07/woolworths-fishy-but-promptly-corrected
```

However, it turns out it’s more convenient to handle the redirection directly from WordPress, with the [Redirection plugin](https://wordpress.org/plugins/redirection). The redirection rules generated above can still be used almost verbatim as RegExps in the plugin’s configuration. One last redirection can also be added for monthly archives to work.

```
*m=(\d*)&y=(\d*) => /20$2/$1
```

I haven’t found a way to catch requests to <tt>comments.php</tt><tt> and </tt><tt>archive.php</tt> (fiddling with WordPress’ <tt>.htaccess</tt> might be required here). However, I assumed that a human should be able to deal with the occasionnal 404 until search engines have refreshed their cache, and didn’t care anymore.

# From BlogSum

While I was rather relieved to get rid of SimplePHPBlog in light of some security vulnerabilities, I was a bit sad to forgo Blogsum. It is a neat blogging engine which Just Works.

Perhaps it even works so well that nobody before has had the need to write an import script for WordPress. So I did. It was an interesting exercise in Ruby and ActiveRecord, connecting to two databases (and two backends) at once.

I bootstrapped the ActiveRecord models with [RMRE](https://github.com/bosko/rmre), which reverse-engineers the database tables into Ruby models.

```
$ rmre19 -a sqlite3 -d ~/site.db  -o . --dump-schema blogsum-schema.rb
Dumping schema to blogsum-schema.rb...
$ rmre19 -a sqlite3 -d ~/site.db  -o . /
Generating models...
```

It’s a good starting point, but complex relationships between tables on the WordPress side (and a rather haphazard field-naming convention, or lack thereof) required some more manual specification.

Once done, it was trivial to write the import logic to [extract data from Blogsum and push it to WordPress](https://scm.narf.ssji.net/git/scripts/tree/Blogsum2WP.rb). So much, in fact, that I didn’t realise that the script had successfully completed the import when it did!

Anyway, this is two blogging platforms down, one (maybe) still to go, and much more flexibility with less headaches in the process.

**Update**: It is probably a good idea to redirect the RSS/Atom feed URLs.

**Update 2**: A redirection from <tt>/Tags/(.\*)</tt> to <tt>/tag/$1</tt> also makes wonders for old Blogsum URLs.