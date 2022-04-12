#! /usr/bin/env python3

import os

curr_location = os.path.dirname(os.path.realpath(__file__))
getAbsPath = lambda x, y: os.path.join(curr_location, x, y)

VERSION = "2.0"
VERSION_URL = "https://raw.githubusercontent.com/IPi-Radio/IPi-Radio/master/VERSION"

STATIONS = getAbsPath("settings", "stations.json")
SETTINGS = getAbsPath("settings", "settings.json")
QML = getAbsPath("ui", "App.qml")
ICON = getAbsPath("lib", "favicon.png")

SELECTION_TIMEOUT = 5*1000
