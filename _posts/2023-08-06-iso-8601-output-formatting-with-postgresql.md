---
id: 950
title: 'ISO-8601 output formatting with PostgreSQL'
date: '2023-08-06T00:06:45+10:00'
author: 'Olivier Mehani'
excerpt: 'ped into a slight issue with timestamp formatting. PostgreSQL supports many date/time formats, but no native support to output ISO-8601 UTC time & date format. Fortunately, StackOverflow had a solution, including some notes about how to handle timestamps with timezones.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=950'
permalink: /2023/08/06/iso-8601-output-formatting-with-postgresql/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '26'
categories:
    - code
    - tip
tags:
    - database
    - PostgreSQL
    - SQL
---

When migrating a database from MySQL to PostgreSQL, I bumped into a slight issue with timestamp formatting. [PostgreSQL supports many date/time formats](<http://PostgreSQL supports many date/time formats>), but no native support to output [ISO-8601](https://www.iso.org/iso-8601-date-and-time-format.html) [UTC time &amp; date format](https://en.wikipedia.org/wiki/ISO_8601) (e.g., 2023-08-05T13:54:22Z), favouring consistency with [RFC3339](https://tools.ietf.org/html/rfc3339) instead.

> ISO 8601 specifies the use of uppercase letter T to separate the date and time. PostgreSQL accepts that format on input, but on output it uses a space rather than T, as shown above. This is for readability and for consistency with RFC 3339 as well as some other database systems. https://tools.ietf.org/html/rfc3339

Fortunately, [StackOverflow had a solution](https://stackoverflow.com/a/39009064), including some [notes about how to handle timestamps with timezones](https://stackoverflow.com/questions/39008759/select-timestamptz-as-utc-zulu-string#comment65370687_39009064).

```
SELECT to_char(now() AT TIME ZONE 'Etc/Zulu', 'yyyy-mm-dd"T"hh24:mi:ss"Z"');
```