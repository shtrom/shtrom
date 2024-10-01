---
id: 1051
title: 'Scheduled events on Multisite Bitnami WordPress'
date: '2023-11-13T11:12:03+11:00'
author: 'Olivier Mehani'
excerpt: 'Using WP-CRON on Bitnami Wordpress images over Web Cron is generally a good idea. But specific steps are needed when dealing with Multisite instances, otherwise scheduled events will silently not run. The trick is to add a dedicated script that iterates over all enabled sites, and processes the events for them all.'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1051'
permalink: '/?p=1051'
---

At the time of this writing, this blog runs on a [Bitnami WordPress](https://bitnami.com/stack/wordpress) image, but I have changed the configuration to run multiple sites (`WP_ALLOW_MULTISITE` and `MULTISITE` in the `wp-config.php`). I realised I had issues running [scheduled events using `DISABLE_WP_CRON`](https://docs.bitnami.com/aws/apps/wordpress/configuration/disable-wordpress-cron/) when the [ActivityPub plugin](https://wordpress.org/plugins/activitypub/) failed to send new posts to subscribers. This was confirmed by the site health dashboard, indicating that scheduled events were late.

As it turns out, when manually running the script with `sudo -u daemon /opt/bitnami/php/bin/php /opt/bitnami/wordpress/wp-cron.php` (with `WP_DEBUG` enabled) complains of an undeclared `HTTP_HOST`, and terminates quickly. As soon as I set that variable in the environment and reran the script, the warning was gone, and the script took longer to run. [All my recent post also made it to the fediverse](https://blog.narf.ssji.net/2023/11/11/trying-the-microblogging-thing/)!

As explained in [this page](https://docs.bitnami.com/aws/apps/wordpress-multisite/configuration/disable-cron/) (which looks a lot like the first one, but is for multisite installations), the longer-term fix is to create a dedicated `/opt/bitnami/wordpress/wp-cron-multisite.php`

```
<?php
// https://docs.bitnami.com/aws/apps/wordpress-multisite/configuration/disable-cron/
require(__DIR__ . '/wp-load.php');
global $wpdb;

$sql = $wpdb->prepare("SELECT domain, path FROM $wpdb->blogs WHERE archived='0' AND deleted ='0' LIMIT 0,300", '');

$blogs = $wpdb->get_results($sql);

foreach($blogs as $blog) {
     $command = "http://" . $blog->domain . ($blog->path ? $blog->path : '/') . 'wp-cron.php';
    $ch = curl_init($command);
    $rc = curl_setopt($ch, CURLOPT_RETURNTRANSFER, FALSE);
    $rc = curl_exec($ch);
    curl_close($ch);
}
```

And call that in the crontab instead of just `wp-cron.php`.