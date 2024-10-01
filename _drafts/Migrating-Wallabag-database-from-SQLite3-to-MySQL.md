---
id: 325
title: 'Migrating Wallabag database from SQLite3 to MySQL'
date: '2023-06-13T12:45:58+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=325'
permalink: '/?p=325'
categories:
    - Uncategorised
---

\* https://stackoverflow.com/a/87531  
\* https://stackoverflow.com/questions/4642535/how-to-remove-carriage-returns-in-a-text-field-in-sqlite#comment40184505\_4642570  
\*\* sqlite3 /tmp/wallabag-nonewlines.sqlite “update wallabag\_entry set content=replace(content, X’0A’, ‘\\n’)”

\*\* sqlite3 /tmp/wallabag-nonewlines.sqlite “update wallabag\_entry set title=replace(title, X’0A’, ‘\\n’)”

\* sqlite3 /tmp/wallabag-nonewlines.sqlite .dump | perl /home/shtrom/sqlite3-to-mysql.pl | mysql -u wallabag -p wallabag -v

```
operator@white-dwarf:/srv/www/wallabag$ sudo -u www bin/console wallabag:install -e prod 
php-5.6:/usr/local/lib/libicuuc.so.12.0: /usr/local/lib/libicudata.so.12.0 : WARNING: symbol(icudt58_dat) size mismatch, relink your program
 Installing wallabag...

Step 1 of 4. Checking system requirements.
+------------------------+--------+----------------+
| Checked | Status | Recommendation |
+------------------------+--------+----------------+
| PDO Driver (pdo_mysql) | OK! | |
| Database connection | OK! | |
| Database version | OK! | |
| curl_exec | OK! | |
| curl_multi_init | OK! | |
+------------------------+--------+----------------+
Success! Your system can run wallabag properly.

Step 2 of 4. Setting up database.
It appears that your database already exists. Would you like to reset it? (y/N)y
Droping database, creating database and schema
Clearing the cache

Step 3 of 4. Administration setup.
Would you like to create a new admin user (recommended) ? (Y/n)s
Step 4 of 4. Config setup.

wallabag has been successfully installed.
Just execute `php bin/console server:run --env=prod` for using wallabag: http://localhost:8000
```