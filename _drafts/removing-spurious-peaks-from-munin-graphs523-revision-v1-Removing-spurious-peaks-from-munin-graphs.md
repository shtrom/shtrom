---
id: 675
title: 'Removing spurious peaks from munin graphs'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=675'
permalink: '/?p=675'
---

Every now and then, some spurious peaks show up on munin graphs. The peaks are order of magnitude higher than the expected range of the data. This particularly happens with DERIVE plugins, that are notably used for network interfaces.

One way to fix this, [as suggested by Steve Schnepp](https://grokbase.com/t/sf/munin-users/09bqzv8rq9/high-peak-in-network-graph-how-to-prevent-it#200911240vzx9jgws1fdek4v2508nqfmsr) (and [in the faq](http://munin-monitoring.org/wiki/faq#Q:Ieditedmyplugintohaveminmaxvaluesbuttheyarenottakenintoaccount)), is to set the maximum straight into the RRD database, and then let it reprocess the data to honour this maximum.

```
RRD_FILE=/var/lib/munin/example.net/host-if_bytes-send-d.rrd
rrdtool tune ${RRD_FILE} --maximum 42:${MAXIMUM_VALUE}
(rrdtool dump ${RRD_FILE} | rrdtool restore --range-check - ${RRD_FILE}.new) && \
mv -i ${RRD_FILE} ${RRD_FILE}.bak && \
mv ${RRD_FILE}.new ${RRD_FILE}
```

`42` is the datasource name that munin uses.

As for the `MAXIMUM_VALUE`, a conservative value for network devices is to use the bandwidth of the backplane. So, for a 20Gbps backplane, one could use `MAXIMUM_VALUE=$((20*1000*1000*1000/8))` (note the division by 8, as the plugin internally stores bytes, and converts them to bits using `CDEF`s when graphing).

**UPDATE (2021-06-04):** Of course, for single interfaces, rather than the total, you should set the maximum value to the speed of the interface.

**UPDATE (2021-06-02):** Sometimes, occasional peaks within the `MAXIMUM_VALUE` but orders of magnitude beyond usual use need to be cleared. A bit of `sed`ing can help, by replacing the high magnitude numbers with `NaN`s.

```
RANGE='[0-9.]\+e+0[6789]'
rrdtool dump ${RRD_FILE} \
  | sed "s/<v>${RANGE}/<v>NaN/" \
  | rrdtool restore --range-check - ${RRD_FILE}.new
```

**UPDATE (2021-06-08):** Correct the `MAXIMUM_VALUE` calculation and add a note about bits and byte conversion.