---
id: 932
title: 'Internet uplink and quota monitoring with HomeAssistant'
date: '2023-07-04T00:09:32+10:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=932'
permalink: /2023/07/04/internet-uplink-and-quota-monitoring-with-homeassistant/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '83'
image: /wp-content/uploads/sites/3/2023/07/image.png
categories:
    - code
    - sysadmin
tags:
    - HomeAssistant
    - monitoring
    - 'smart home'
    - SNMP
---

I finally fell for the smart-home mania when I needed to read a [few Zigbee climate sensors, and started using Home Assistant](https://consumeristadventures.info/2022/11/12/product-reviews-smart-home/). There was no return from it, and I gradually grew the number of sensors and automations. This is all the easier thanks to a [very active community site, offering many a recipe and troubleshooting advice](https://community.home-assistant.io/). This is where I found a [bandwidth monitor based on SNMP metrics](https://community.home-assistant.io/t/snmp-bandwidth-monitor/7122) that has been functional for a while.

My ISP, [Internode (no longer the awesome service it used to be 10 years ago)](https://consumeristadventures.info/2012/06/04/internodes-customer-service-is-a-breath-of-fresh-air/), has become increasingly flaky, silently dropping support for their Customer Tools API. This API was useful to track quota usage in a number of tools, including my own [Munin plugin](https://gallery.munin-monitoring.org/plugins/munin-contrib/internode_usage/). Because of this, I unwittingly, and without warning, went beyond my monthly quota this month. I had to double my monthly bill to buy additional data blocks to tie me over.

It became obvious that I needed a new way to track my usage. What could be better than HomeAssistant, which was already ingesting SNMP data from the router? I [posted my updated solution in the original thread](https://community.home-assistant.io/t/snmp-bandwidth-monitor/7122/86), but thought that it might be worth duplicating here.

Here is my updated config, which I placed in `config/packages/internet_speed.yaml`. For clarity, I will build it up in a few additive sections (note the `...` indicating that existing content from the previous sections should remain).

First, while reading around, I realised that [HA now supports templated sensors](https://www.home-assistant.io/integrations/template#configuration-variables), which means the `input_number` and automation helpers suggested in the early post are no longer needed.

{% raw %}
```
sensor:
  # Based on https://community.home-assistant.io/t/snmp-bandwidth-monitor/7122; This hasn't changed
  # Get raw SNMP readings
  - platform: snmp
    name: snmp_wan_in
    host: 192.2.0.1
    baseoid: 1.3.6.1.2.1.2.2.1.10.20  # the second last integer should match your WAN interface
  - platform: snmp
    name: snmp_wan_out
    host: 192.2.0.1
    baseoid: 1.3.6.1.2.1.2.2.1.16.20  # the second last integer should match your WAN interface

  # Calculate the mean from templated speed sensors below
  - platform: statistics
    unique_id: internet_speed_down_mean
    name: 'Internet Speed Down (mean)'
    entity_id: sensor.internet_speed_down
    state_characteristic: mean
    sampling_size: 20
  - platform: statistics
    unique_id: internet_speed_up_mean
    name: 'Internet Speed Up (mean)'
    entity_id: sensor.internet_speed_up
    state_characteristic: mean
    sampling_size: 20

template:
  # Templated internet_speed_down and internet_speed_up sensor, that update automatically when the snmp sensors do
  - trigger:
    - platform: state
      entity_id: sensor.snmp_wan_in
    sensor:
    - unique_id: internet_speed_down
      name: 'Internet Speed Down'
      state: >
        {{ (
          ( (trigger.to_state.state | int - trigger.from_state.state | int) * 8 / 1000000 )
          / ( as_timestamp(trigger.to_state.last_updated) - as_timestamp(trigger.from_state.last_updated))
          ) | round(2)
        }}
      state_class: measurement
      device_class: data_rate
      unit_of_measurement: 'Mbit/s'
      icon: mdi:download
  - trigger:
    - platform: state
      entity_id: sensor.snmp_wan_out
    sensor:
    - unique_id: internet_speed_up
      name: 'Internet Speed Up'
      state: >
        {{ (
          ( (trigger.to_state.state | int - trigger.from_state.state | int) * 8 / 1000000 )
          / ( as_timestamp(trigger.to_state.last_updated) - as_timestamp(trigger.from_state.last_updated))
          ) | round(2)
        }}
      state_class: measurement
      device_class: data_rate
      unit_of_measurement: 'Mbit/s'
      icon: mdi:upload
```
{% endraw %}

Based on the SNMP sensor, I also created an `total_increasing` counter of the sum of up and down traffic, as well as a monthly-resetting (on the 23rd) utility meter.

{% raw %}
```
template:
  [...]
  - sensor:
    - unique_id: internet_total_usage
      name: 'Internet Total Usage'
      state: >
        {{ (
          (states("sensor.snmp_wan_in")|int + states("sensor.snmp_wan_out")|int)
          / (1024*1024)
          ) | round(2)
        }}
      state_class: total_increasing
      device_class: data_size
      unit_of_measurement: 'MiB'
      icon: mdi:chart-bell-curve-cumulative

utility_meter:
  internet_usage:
    unique_id: internet_usage
    name: "Internet Usage"
    source: sensor.internet_total_usage
    cycle: monthly
    offset:
      days: 22  # offset from day 1
    periodically_resetting: true
```
{% endraw %}

For ease of update of the monthly quota, I added a couple of `input_number` to set the quota and the reset date (unfortunately, I haven’t found a way to reuse it in the `utility_meter`)

```
input_number:
  internet_quota:
    name: "Internet Quota"
    initial: 500000
    min: 0
    max: inf
    icon: mdi:chart-multiline
    mode: box
    unit_of_measurement: MiB
  internet_quota_rollover_day:
    name: "Internet Quota Rollover Day"
    initial: 23
    min: 1
    max: 31
    icon: mdi:calendar-refresh
    mode: box
```

This allowed me to calculate an ideal usage given the date, *i.e.*, if my current usage is above the ideal usage, I’m at risk of exceeding the quota before the end of the month. A `binary_sensor` just does that comparison; if it’s `on`, I’m in trouble.

{% raw %}
```
template:
  [...]
    - unique_id: internet_ideal_usage
      name: 'Internet Ideal Usage'
      state: >
        {% set day = now().date().day %}
        {% set month = now().month %}

        {% set rollover = states("input_number.internet_quota_rollover_day")|int %}

        {% if day >= rollover %}
          {% set start = now().date().replace(day=rollover) %}
          {% set next_month = start.replace(day=28) + timedelta(days=4) %}
          {% set end = next_month.replace(day=rollover) %}

        {% else %}
          {% set end = now().date().replace(day=rollover) %}
          {% set last_month = end.replace(day=1) - timedelta(days=1) %}
          {% set start = last_month.replace(day=rollover) %}

        {% endif %}

        {% set full_period = (as_timestamp(end) - as_timestamp(start))|int %}
        {% set current_period = (as_timestamp(now()) - as_timestamp(start))|int %}
  
        {% set quota = states("input_number.internet_quota")|int %}

        {% set ideal = ((quota*current_period)/full_period)|float %}

        {{ ideal }}
      state_class: total_increasing
      device_class: data_size
      unit_of_measurement: 'MiB'
      icon: mdi:chart-bell-curve-cumulative
  - binary_sensor:
    - unique_id: internet_usage_warning
      name: 'Internet Usage Warning'
      state: '{{ (states("sensor.internet_usage")|int) > (states("sensor.internet_ideal_usage")|int) }}'
      icon: >
        {% if is_state('binary_sensor.internet_usage_warning', 'on') %}
        mdi:alert
        {% else %}
        mdi:check-circle-outline
        {% endif %}
```
{% endraw %}

And to tie it neatly, I added an automatic (daily) notification in case the warning is triggered.

{% raw %}
```
automation:
  - alias: "Notification: Internet usage"
    description: ""
    trigger:
      - platform: state
        entity_id:
          - binary_sensor.internet_usage_warning
        for:
          hours: 1
        from: "off"
        to: "on"
    condition:
      - >-
        {{ now() - (state_attr(this.entity_id, 'last_triggered') or
        datetime.datetime(1, 1, 1, 0, 0) ) > timedelta(hours=12) }}
    action:
      - service: notify.persistent_notification
        data:
          title: Internet usage over quota
          message: >
            {{state_attr('sensor.internet_usage', 'friendly_name')}}
            ({{states('sensor.internet_usage')|round(2)}} MiB) is higher than ideal
            ({{states('sensor.internet_ideal_usage')|round(2)}} MiB)

            Turn things off!
    mode: single
```
{% endraw %}

Et voilà! No going over quota now!

<div class="wp-block-image"><figure class="aligncenter size-full">![A few HomeAssistant cards showing SNMP monitoring of speed and quota of an upstring ISP.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/07/image.png)</figure></div>