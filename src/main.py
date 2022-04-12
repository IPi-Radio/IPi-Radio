#! /usr/bin/env python3

import os
import sys
import json
import time
import socket
from multiprocessing import Process

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

import server
from radio import Player
from constants import QML, SETTINGS, STATIONS

def parseSettings() -> dict:
    try:
        with open(SETTINGS, "r") as f:
            settings: dict = json.load(f)
    except FileNotFoundError:
        print(f"Could not find settings file: {SETTINGS}")
        sys.exit(-1)

    return settings

def checkNetwork() -> tuple:
    print("checking network connection...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect( ("1.1.1.1", 80) )
            ip = s.getsockname()[0]
    except:
        return False

    if settings.get("IP") not in ["DHCP", "AUTO", "auto"]:
        ip = settings.get("IP")

    port = settings.get("Port")
    if 0 < port < 65535:
        ip_port = (ip, port)
    else:
        return False
    
    return ip_port

def initWebserver(ip_port: tuple) -> Process:
    print(f"starting HTTP server on: {ip_port[0]}:{ip_port[1]}")

    webserver = Process(
        target=server.run, args=(ip_port,SETTINGS,STATIONS))
    webserver.start()

    print("webserver started")
    return webserver


if __name__ == "__main__":
    global settings
    settings = parseSettings()
    webserver = None


    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.breeze"
    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"

    # this is from https://doc.qt.io/qt-5/embedded-linux.html
    # run without X server
    #os.environ["QWS_DISPLAY"] = r"linuxfb:fb=/dev/fb0"
    if settings.get("useFramebuffer") and settings.get("framebuffer"):
        os.environ["QT_QPA_PLATFORM"] = f'linuxfb:fb={settings["framebuffer"]}'

    while not (ip_port := checkNetwork()):
        print("ERROR: network not available, retrying...")
        time.sleep(1)

    app = QGuiApplication(sys.argv)
    player = Player(ip_port)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", player)
    engine.quit.connect(app.quit)
    #engine.load("ui/App.qml")
    engine.load(QML)

    if not engine.rootObjects():
        sys.exit(-1)
    
    if settings.get("runWebserver") == True:
        webserver = initWebserver(ip_port)
    else:
        player.setWebserverUrl( ("webserver disabled", "") )

    if settings.get("autotimer"):
        player.setAutoTimer(True)

    exitcode = app.exec()
    if webserver != None:
        print("stopping webserver...")
        webserver.terminate()

    sys.exit(exitcode)
