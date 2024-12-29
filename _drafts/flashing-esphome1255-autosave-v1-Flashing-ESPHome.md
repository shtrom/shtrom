---
id: 1452
title: 'Flashing ESPHome'
date: '2024-03-11T18:30:09+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1452'
permalink: '/?p=1452'
footnotes:
    - ''
---

- Working on the [4–20mA Current Loop Rain Water Tank Sensor](https://blog.narf.ssji.net/2023/11/11/4-20ma-current-loop-rain-water-tank-sensor/)
- No galvanic insulation on the ESP32-POE 
    - Dangerous to connect USB and PoE ethernet at the same time
    - Found a non-PoE switch to put in between 
        - Powered *that* with PoE
- Can’t use the [ESPHome dashboard](https://esphome.io/guides/getting_started_hassio#installing-esphome-dashboard) on HA deployed in Docker
- Can’t use the [Web Dashboard](https://esphome.io/guides/getting_started_command_line) in Firefox anyway, due to the lack of WebSerial support
- Can work from within the container, and expose the USB device to it by mounting it as a volume 
    - `privilege`d mode is likely mandatory

```
version: '3'
services:
  esphome:
    container_name: esphome
    image: ghcr.io/esphome/esphome
    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
      - /dev/ttyUSB0:/dev/ttyUSB0
    restart: always
    privileged: true
    network_mode: host
    environment:
      - USERNAME=test
      - PASSWORD=ChangeMe
```

- run and connect to it

```
~/water-tank-sensor$ docker-compose exec esphome bash
root@docker:/config# esphome wizard water-sensor.yaml
<interactive questions>
(name): water-tank-sensor 
(ESP32/ESP8266/BK72XX/RTL87XX): esp32
(board): esp32-poe
(ssid): wifi
(PSK): hunter2
(password): hunter2
```

- Editing config 
    - Example for Olimex ESP32-PoE <https://esphome.io/components/ethernet.html?highlight=ethernet#configuration-examples>
    - Example config using ethernet: <https://devices.esphome.io/devices/Genvex-Nibe-AlphaInnotec-heat-recovery-ventilation>
    - esphome refuses to use GPIO 36, but it’s the only ADC GPIO on the UEXT connector 
        - was happy with it the second time, after building on a separate port, then restoring the original one and rebuilding 🤷
    - will need to put the full config somewhere when good

```
root@docker$ esphome compile water-tank-sensor.yaml 
root@docker$ esphome upload water-tank-sensor.yaml 
```

- <https://esphome.io/components/sensor/adc.html> “the usable ADC range was from ~0.075V to ~3.12V (with the `attenuation: auto` setting)” 
    - R\_min=0.075/0.004=18.75 ohm; R\_max=3.12/.02 156 ohm
    - will probably need to use 100 ohm
- Got it going in Home Assistant; the data is rubbish because it needs calibration, and likely because the sensor is running below nominal voltage
- Next steps: find where to find enough voltage to drive the sensor, change resistor, calibrate

<figure class="wp-block-gallery has-nested-images columns-1 wp-block-gallery-98 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbf64c64a"}" data-wp-interactive="core/image">![A messy set of electronic components: an ESP32-POE connected to a small desktop switch, itself connected to a PoE splitter.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/PXL_20240119_131359405-smol-1024x768.jpg)<button aria-haspopup="dialog" aria-label="Enlarge image: A messy set of electronic components: an ESP32-POE connected to a small desktop switch, itself connected to a PoE splitter." class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure><figure class="wp-block-image size-large wp-lightbox-container" data-wp-context="{"imageId":"6770cbf64cb63"}" data-wp-interactive="core/image">![Screenshot of a Home Assistant integration dashboard showing some voltage and volume measurement from an ESPHome-based Water tank sensor](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-from-2024-01-20-00-22-25-1024x351.png)<button aria-haspopup="dialog" aria-label="Enlarge image: Screenshot of a Home Assistant integration dashboard showing some voltage and volume measurement from an ESPHome-based Water tank sensor" class="lightbox-trigger" data-wp-init="callbacks.initTriggerButton" data-wp-on-async--click="actions.showLightbox" data-wp-style--right="state.imageButtonRight" data-wp-style--top="state.imageButtonTop" type="button"> <svg fill="none" height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg"><path d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z" fill="#fff"></path></svg></button></figure></figure>