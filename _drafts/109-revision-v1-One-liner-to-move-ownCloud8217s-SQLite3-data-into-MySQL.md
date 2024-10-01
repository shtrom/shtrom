---
id: 803
title: 'One-liner to move ownCloud&#8217;s SQLite3 data into MySQL'
date: '2023-02-09T23:48:45+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=803'
permalink: '/?p=803'
---

As seen in [this post](http://laurentbois.wordpress.com/2008/10/13/tip-export-sqlite-database-convert-and-import-into-mysql/ "Tip: export sqlite database, convert and import into mysql"), with some alterations based on my experience.

```
sqlite3 owncloud.db .dump | sed '/BEGIN TRANSACTION;/d;/COMMIT/d;/PRAGMA/d;/sqlite_sequence/d;s/"/`/g;s/AUTOINCREMENT/auto_increment/g;s/CLOB/LONGTEXT/g' | mysql -uroot -p owncloud
```

There is however one trick: while [ownCould](http://owncloud.org/) uses `CLOB`s in SQLite3, MySQL doesn’t have it. Rather, there appears to be some logic depending on the expected length of the text content to choose the MySQL type for that column. Here, we are conservative, and always choose the default, `LONGTEXT`, hoping this will be sufficient.

Some issues emerged: table names were prefixed with `oc_`, which doesn’t appear to be the defaut, but can be fixed in the `config.php` with

```

  'dbtableprefix' => 'oc_',
```

Another problem seems to be that the `id` field of the `[oc_]jobs` table lost its `AUTOINCREMENT` attribute in the process; not sure why. Finally, users cannot log in.