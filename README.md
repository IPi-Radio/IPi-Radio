# IPi-Radio-core

Simple and easy IP Radio for Raspberry Pi

### Showcase

(video)

(screenshots)

### How to install

###### Requirements

- Raspberry Pi (tested on 3 and 4, but older should work too)
- SDcard >= 4GB
- Screen with at least 800x480 is recommended (touchscreen is optional)

###### Pre Install

- Raspberry Pi OS **lite** is recommended
- connect your Pi to the network
- `sudo raspi-config`
  - `1 System Options`
    - `S2 Audio` select the correct audio device
    - `S5 Boot / Auto Login` select `B2 Console Autologin`
    - `S6 Network at Boot` select `Yes`
  - `2 Display Options` > `D5 Screen Blanking` select `No`
- make sure all packages are up to date `sudo apt update && sudo apt dist-upgrade`

###### Install IPi-Radio

```bash
# install dependencies
sudo apt install git python3 python3-pyqt5 python3-vlc vlc pulseaudio qt5-style-kvantum qt5-style-plugins
# Note: you will need at least Python 3.6 and vlc 3.0.0

# reboot
sudo reboot now

# clone this repo
git clone https://github.com/IPi-Radio/IPi-Radio.git

# add IPi-Radio to autostart
sudo nano /etc/rc.local
    # insert above(!) the exit 0 statement:
    python3 /path/to/repo/IPi-Radio/src/IPi-Radio.py
```

###### Post Install

optionally you can change some settings, for that you open `IPi-Radio/src/settings/settings.json`

- change `framebuffer` if you have a screen, that is not using default `/dev/fb0`
- set `IP` or `Port` of the webserver or disable it by setting `runWebserver` to `false`
- change `touchOptimize` to `false` if you don't want touchscreen optimization

you also may want to adjust the brightness of your screen:

`echo n | sudo tee /sys/class/backlight/rpi_backlight/device/backlight/rpi_backlight/brightness`

while `n` is a value between 0 and 255

#### Any Linux powered machine

- change settings in `src/settings/settings.json`
  - set `useFramebuffer` to `false`
  - (optional) set `IP` or `Port` of the webserver
- start with `python3 src/IPi-Radio.py`
