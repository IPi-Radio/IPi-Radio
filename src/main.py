#! /usr/bin/env python3

import sys
import signal
import json
import time
import socket
from threading import Thread

from http.server import HTTPServer

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialog, 
    QWidget,
    QLabel,
)
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

def checkNetwork(settings: dict) -> tuple:
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


def initWebserver(player: Player, settings: dict):
    player.waitingNetworkState.emit()

    while not (ip_port := checkNetwork(settings)):
        print("ERROR: network not available, retrying...")
        time.sleep(1)

    time.sleep(1)

    player.waitingServerState.emit()

    if settings.get("runWebserver"):
        print(f"starting HTTP server on: {ip_port[0]}:{ip_port[1]}")

        webserver = server.initServer(ip_port, SETTINGS, STATIONS)
        webserverThread = Thread(target=webserver.serve_forever, daemon=True)
        webserverThread.start()

        print("webserver started")

        player.setWebserverUrl(*ip_port)
    else:
        player.setWebserverUrl( *("webserver disabled", "") )

    if settings.get("autotimer"):
        player.setAutoTimer(True)

    player.waitingDone.emit()


if __name__ == "__main__":
    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.breeze"
    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"

    # this is from https://doc.qt.io/qt-5/embedded-linux.html
    # run without X server
    #os.environ["QWS_DISPLAY"] = r"linuxfb:fb=/dev/fb0"
    #if settings.get("useFramebuffer") and settings.get("framebuffer"):
    #    os.environ["QT_QPA_PLATFORM"] = f'linuxfb:fb={settings["framebuffer"]}'

    settings = parseSettings()

    app = QApplication(sys.argv)
    print(app.platformName())

    player = Player()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", player)
    engine.load(QML)

    if not engine.rootObjects():
        sys.exit(1)

    Thread(target=initWebserver, args=(player, settings)).start()

    def close(*args, **kwargs):
        print("exit triggered")
        app.exit(0)

    signal.signal(signal.SIGINT, close)
    signal.signal(signal.SIGTERM, close)

    sys.exit(app.exec_())
