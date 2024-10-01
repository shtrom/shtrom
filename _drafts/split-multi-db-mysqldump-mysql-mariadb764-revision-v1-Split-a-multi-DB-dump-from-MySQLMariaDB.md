---
id: 772
title: 'Split a multi-DB dump from MySQL/MariaDB'
date: '2023-01-14T16:19:47+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=772'
permalink: '/?p=772'
---

I recently had to restore databases from a rough `mysqldump` backup in a piecemeal fashion. One necessity is to `SET` the environment correctly, lest some weird encoding issues happen when restoring the data, leading to failures.

A `sed` one-liner can help for this.

```
DBNAME=mydb
sed -n "/^-- Server version/,/^-- Current Database/p;/^-- Current Database.*${DBNAME}\`/,/^-- Current Database/{p}" mysqldump.sql > ${DBNAME}.sql
```

This extracts SQL from the initial header, to the first database, which contains all the sessions `SET`s. It then captures statements any time the target database is the current one. Note that this doesn’t restore the `GRANT`s.

Befor blindly piping the output SQL into `mysql`, one would be well advised to review the contents of the file, to ensure only the desired modifications are included.