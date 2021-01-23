# IPi-Radio-core

Simple and easy IP Radio for Raspberry Pi

### Showcase

### How to install

###### Requirements

- Linux
- python >= 3.6
- vlc >= 3.0

```bash
# install dependencies
apt install python3 python3-pyqt5 python3-vlc vlc

# clone this repo
git clone https://github.com/IPi-Radio/IPi-Radio-core.git
```

#### Raspberry Pi

Using the official Raspberry Pi OS **lite** without any X server is the recommended setup.

- use `raspi-config` to set your audio device and set boot to **CLI autologin**
- add IPi-Radio to the autostart:
  - add `python3 /path/to/repo/IPi-Radio-core/src/IPi-Radio.py` to `/etc/rc.local`
- (optional) set settings in `src/settings/settings.json`
  - change `framebuffer` if you have a screen, that is not using default `/dev/fb0`
  - set `IP` or `Port` of the webserver

#### Any Linux powered machine

- change settings in `src/settings/settings.json`
  - set `useFramebuffer` to `false`
  - (optional) set `IP` or `Port` of the webserver
- start with `python3 src/IPi-Radio.py`
