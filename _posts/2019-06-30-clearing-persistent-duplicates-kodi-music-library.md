---
id: 416
title: 'Clearing persistent duplicates in the Kodi music library'
date: '2019-06-30T19:43:34+10:00'
author: 'Olivier Mehani'
excerpt: 'Some SQL to clear up duplicate albums in the Kodi music library when cleaning it is just not enough.'
layout: post
guid: 'https://blog.narf.ssji.net/?p=416'
permalink: /2019/06/30/clearing-persistent-duplicates-kodi-music-library/
iawp_total_views:
    - '20'
categories:
    - code
    - fix
    - tip
tags:
    - Kodi
    - MySQL
    - SQL
    - XBMC
---

I’ve been using Kodi (then XBMC) for more than a decade now (yup, “XB” did stand for X Box alright, but now [LibreELEC](https://libreelec.tv/) on a [WeTek Core](https://libreelec.tv/downloads/wetek-core/)). I’ve also had the [library in MySQL](https://kodi.wiki/view/MySQL) for more than half of it. Across migrations, it had developed some quirky content, such as duplicate albums, and some rarities, such as this version of *21*, by Adèle, where the description reminds us that her previous album, *Ixnay on the Hombre*, was only moderately successful on launch; go figure…

As suggested, pretty much everywhere, as the solution for duplicate content in Kodi, I first tried cleaning the library, repeatedly, to no avail. The duplicate albums were still there. One of their noticeable characteristics, though, was that there was always some copy of the album (and in Adèle’s case, the one following *Ixnay*), that did not have any associated tracks. This felt like it could be a good angle to help me clear those up. Enter some SQL.

Comparing both copies of *21* above, I could see that both albums were associated to a different set of songs, and one set of songs (the one that came after *Ixnay*) no longer had a valid path (`strPath`) associated to it. This was sufficient to clear out all those songs.

```
MyMusic72> delete from song
           where idSong in (
                            select idSong
                            from song
                            left join path using(idPath)
                            where strPath is null
                           );
```

That’s all the duplicate songs gone. Next step, albums.

```
MyMusic72> delete from album
           where idAlbum in (
                             select album.idAlbum
                             from album
                             left join song using(idAlbum)
                             where idPath is null
                            );
(1442, "Can't update table 'song' in stored function/trigger because it is already used by statement which invoked this stored function/trigger")
```

Woops. This error is due to the fact that there is a trigger on the `album` table that does something to the `song` table on deletion.

```
MyMusic72> show triggers where `table` = 'album'\G
***************************[ 1. row ]***************************
Trigger              | tgrDeleteAlbum
Event                | DELETE
Table                | album
Statement            | BEGIN  DELETE FROM song WHERE song.idAlbum = old.idAlbum;  DELETE FROM album_artist WHERE album_artist.idAlbum = old.idAlbum;  DELETE FROM album_source WHERE album_source.idAlbum = old.idAlbum;  DELETE FROM art WHERE media_id=old.idAlbum AND media_type='album'; END
Timing               | AFTER
Created              | <null>
sql_mode             | NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
Definer              | xbmc@%
character_set_client | utf8
collation_connection | utf8_general_ci
Database Collation   | utf8_general_ci
```

The workaround is simple. I just used a temporary table to store the result of the sub-request (the IDs of the albums to delete).

```
MyMusic72> create table tmp_album (`idAlbum` int(11) NOT NULL);
MyMusic72> insert into tmp_album (
                                  select album.idAlbum
                                  from album
                                  left join song using(idAlbum)
                                  where idPath is null
                                 );
MyMusic72> delete from album
           where idAlbum in (
                             select idAlbum
                             from tmp_album
                            );
```

And a final spot of cleanup.

```
MyMusic72> drop table tmp_album;
```

And my music library is now free of duplicates!

## EDIT 2019-07-04: Removing more duplicates

Apparently, I was too quick to claim victory. For some reason, I still had some duplicate albums (2 or 3 versions), with all the songs split between the copies.

The solution to that issue was to get a list of all the idAlbum of the duplicates, associate (arbitrarily) all the songs to the first `idAlbum`, and delete all the others.

This is easily done with a few more SQL queries, some of them generated with topical application of [`sed`](https://linux.die.net/man/1/sed), for handy, regular expression-based string modification.

First, let’s get a list of all albums with duplicates (by title and artist), along with the ID of the first album, and a list of all the IDs.

```
MyMusic72> select idAlbum, group_concat(idAlbum) from album group by strAlbum, strArtistDisp having count(1)>1;
```

Using [mycli (a great command-line client for MySQL, with syntax hightlighting and autocompletion)](https://www.mycli.net/), the result of the query can be output as a CSV file, by running those commands before the query.

```
\T csv
\o dupes.csv
```

The data is just what we need:

```
$ head dupes.csv
2209,"2209,8126"
8031,"8031,4494"
8055,"8055,8056,2219"
6003,"6003,6004"
6005,"6005,6006"
7739,"7739,2228"
7844,"7844,2230"
2232,"2232,7663"
7841,"7841,2233"
7842,"7842,2234"
```

In hindsight, the first column is not needed as the data is also at the beginning of the second one, but it doesn’t matter much. With a couple of regexps, we make a series of SQL queries out of it, putting all the songs into the first album.

```
$ sed '1d;s/\([^,]\+\),"\([^"]\+\)"/update ignore song set idAlbum=\1 where idAlbum in (\2);/' dupes.csv > dedup.sql
$ head dedup.sql
update ignore song set idAlbum=2209 where idAlbum in (2209,8126);
update ignore song set idAlbum=8031 where idAlbum in (8031,4494);
update ignore song set idAlbum=8055 where idAlbum in (8055,8056,2219);
update ignore song set idAlbum=6003 where idAlbum in (6003,6004);
update ignore song set idAlbum=6005 where idAlbum in (6005,6006);
update ignore song set idAlbum=7739 where idAlbum in (7739,2228);
update ignore song set idAlbum=7844 where idAlbum in (7844,2230);
update ignore song set idAlbum=2232 where idAlbum in (2232,7663);
update ignore song set idAlbum=7841 where idAlbum in (7841,2233);
update ignore song set idAlbum=7842 where idAlbum in (7842,2234);
```

I found the `ignore` to be necessary as, in some cases, there were a few song duplicates that were violating some `unique` constraints. We just need to source that file, and run the queries through the DB. I made backups first, this time.

```
MyMusic72> create table song_bak like song;
MyMusic72> insert into song_bak select * from song;
MyMusic72> create table album_bak like album;
MyMusic72> insert into album_bak select * from album;
MyMusic72> \. dedup.sql
```

Now that (most of, due to the `ignore`) the duplicate albums no longer have songs associated to them, we can clear them. We create the list of deletion queries with another `sed` run.

```
$ sed '1d;s/.*,"[^,]\+,\([^"]\+\)"/delete from album where idAlbum in (\1);/' dupes.csv > delalbums.sql
$ head delalbums.sql
delete from album where idAlbum in (8126);
delete from album where idAlbum in (4494);
delete from album where idAlbum in (8056,2219);
delete from album where idAlbum in (6004);
delete from album where idAlbum in (6006);
delete from album where idAlbum in (2228);
delete from album where idAlbum in (2230);
delete from album where idAlbum in (7663);
delete from album where idAlbum in (2233);
delete from album where idAlbum in (2234);
```

And we run them

```
MyMusic72> \. delalbums.sql
```

And I now have far fewer duplicates (and hopefully none)!