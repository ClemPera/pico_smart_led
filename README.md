# pico_smart_led
Controlling an LED strip with Pico W and Home Assistant (On desktop or phone!) using MQTT

## Summary
You can control a LED strip with a Pico W an Home Assistant easily. It works fine but there's issues (see bellow) and it can be improved a lot. It was a fun project to make but for a more reliable alternative I would recommend to use [ESPHome](https://esphome.io/guides/getting_started_hassio.html).

## Material
- Pico W
- Local server (or Raspberry Pi) with docker Home Assistant and mosquitto

## Features 
- **Control brightness** via Home Assistant
- **Color picker** via Home Assistant
- **Watchdog**: Restart when there's any issue to make it always available 

## Issues:
- **Mosquitto**: I had reliability/slowdowns with the official docker of mosquitto (even locally) so I switched to `broker.mqtt.cool` to have an already configured and functionnal BUT it's not secure, anyone could turn on or change color of the LEDs and two devices without any changes in the code would turn on both of the devices.
- **MQTT**: MQTT is great to send sensor data but is not reliable to be used to react to data received at the same time. Data sent to the device will often be lost (e.g. sliding the color picker). There's also some disconnections so data sent are lost before the device reconnect. An rest API would be a lot more reliable.
- **Power issues**: The Pico W doesn't give enough amps to have a lot of luminosity. You could use an external power source with a relay to power the LEDs correctly
- **Design**: It's not a great design, you see the cables and the pico, and if you touch it you could unplug the cables. You could solder the cables directly to the Pico and could design and print a 3D box to protect everything.

## Some pictures
![Pico plugged to a LED strip on a wall](/Pictures/PicoOnWall.jpg)
![Home Assistant color picker](/Pictures/HomeAssistant2.png)
![Pico and cable plugged](/Pictures/Pico.jpg)
![LED Strip turned on](/Pictures/LEDStrip.jpg)
![Home Assistant with brightness purcentages](/Pictures/HomeAssistant1.png)