---
id: 680
title: 'Using munin-async to reduce gaps in monitoring&#8230; and system load'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=680'
permalink: '/?p=680'
---

I use [Munin](http://munin-monitoring.org/) to monitor a few machines, and bubble up alerts when issues show up. It’s pretty good, easy to set up, and has a large number of [contributed plugins to monitor pretty much everything](https://github.com/munin-monitoring/contrib/). If still out of luck, it’s [easy enough to write your own](http://guide.munin-monitoring.org/en/latest/develop/plugins/howto-write-plugins.html).

To ease the task of viewing the data, each machine runs `<a href="http://guide.munin-monitoring.org/en/latest/reference/munin-node.html">munin-node</a>`, but only a couple of masters do the data collection with `<a href="http://guide.munin-monitoring.org/en/latest/reference/munin-update.html">munin-update</a>`. This works reasonably well, except that machines monitored by more than one server need to work extra time to provide the same data to both.

Fortunately, [Munin 2.0 introduced a proxy mode](http://guide.munin-monitoring.org/en/latest/node/async.html), allowing to decouple running the plugins to collect fresh data (with `<a href="http://guide.munin-monitoring.org/en/latest/reference/munin-asyncd.html">munin-asyncd</a>`) from giving that data to collection servers (via `<a href="http://guide.munin-monitoring.org/en/latest/reference/munin-async.html">munin-async</a>`).

Setting this up is relatively easy, and the benefits show quickly, in the form of a reduced collection time, and fewer gaps in the data.

<div class="wp-block-image"><figure class="aligncenter">![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2019/09/wd-async-munin_stats-day.png)<figcaption>Reduced update time for the master, and no more gaps in the data.</figcaption></figure></div>Surprisingly it also showed as a substantially reduced load on low-power machines. But beware of the `--fork` parameter to `munin-asyncd`.

## Direct remote monitoring

The usual setup (generally as additional files in `/etc/munin/munin-conf.d`) for direct monitoring is that a master connects to a slaves, either directly.

```
[example.net;munin-slave]
address munin-slave.example.net
```

Or via an SSH tunnel, so as not to expose `munin-node` to the outside world.

```
[example.net;munin-slave]
address ssh://munin@munin-slave.example.net -W localhost:4949
```

For this second use-case to work, a user, say `munin`, needs to be set-up on the slave, that allows the master to log-in with a private key. This is done in `~munin/.ssh/authorized_keys`.

```
command="/bin/false",no-agent-forwarding,no-pty,no-user-rc,no-X11-forwarding,permitopen="localhost:4949" ssh-ed25519 AAAA... munin@master.example.net
```

This works nicely (once keys have been distributed and accepted), and the `munin` user on the slave doesn’t even need a valid shell.

## Asynchronous remote monitoring

To switch to asynchronous monitoring, the first step is to install and/or enable the `munin-asyncd` service. The package and command to do so varies depending on distribution and OS, so this is left as an exercise to the reader.

Once done, though, changes are minimal. The slave needs to force `munin-async --spoolfetch` to be run when the master connects with its key.

```
command="/usr/share/munin/munin-async --spoolfetch",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty,no-user-rc ssh-ed25519 AAAA... munin@master.example.net
```

And the master no longer needs tunnelling.

```
[example.net;munin-slave]
address ssh://munin@munin-slave.example.net:22
```

One mildly annoying point is that the `munin` user on the slave can no longer have an invalid shell, such as `/bin/false`. Otherwise, the SSH connection terminates immediately. Using `/bin/sh` instead is sufficient to fix the issue. Provided the user’s `authorized_keys` remains simple and limits access, and no password access is allowed, this should however remain sufficiently secure.

This is however sufficient to reduce the processing time of `munin-update` on the master, as well as the load on the slaves, which now only need to run the plugins once per period, rather than once per period per master.

<div class="wp-block-image"><figure class="aligncenter">![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2019/09/wd-async-cpu-day.png)<figcaption>Reduced load on low-power machines, as the plugins only run once per update period.</figcaption></figure></div>### Forking updates may not be all the rage

In one confusing case (on OpenBSD), the load on the machine greatly increased when switching to `munin-asyncd`. Investigations revealed that this was due to all plugins running at the same time, in parallel, whenever the daemon woke up.

This is due to the [startup script using the ](https://cvsweb.openbsd.org/ports/net/munin/pkg/munin_asyncd.rc?rev=1.5&content-type=text/x-cvsweb-markup)`<a href="https://cvsweb.openbsd.org/ports/net/munin/pkg/munin_asyncd.rc?rev=1.5&content-type=text/x-cvsweb-markup">--fork</a>`[ option](https://cvsweb.openbsd.org/ports/net/munin/pkg/munin_asyncd.rc?rev=1.5&content-type=text/x-cvsweb-markup), which forks a new process for each plugin, rather than querying them in sequence. Removing this option (in `/etc/rc.d/munin_asyncd`) fixed the issue nicely.

<div class="wp-block-image"><figure class="aligncenter">![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2019/09/wd-async-load-day.png)<figcaption>munin-async –fork allows to parallelise plugin queries, but at the cost of spikes in load when it does so.</figcaption></figure></div>