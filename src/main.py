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


class Startup(QDialog):
    
    oninit = pyqtSignal()
    onNetworkCheck = pyqtSignal()
    onFinish = pyqtSignal()

    def __init__(self):
        super().__init__()

        label = QLabel("LOADING", self)
        label.resize(600, 200)
        label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("background-color: #101010; color: white;")

        self.oninit.connect(lambda: label.setText("STARTING IPi-Radio"))
        self.onNetworkCheck.connect(lambda: label.setText("WAITING FOR NETWORK"))

        self.onFinish.connect(self.accept)

if __name__ == "__main__":
    global settings

    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.breeze"
    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"

    # this is from https://doc.qt.io/qt-5/embedded-linux.html
    # run without X server
    #os.environ["QWS_DISPLAY"] = r"linuxfb:fb=/dev/fb0"
    #if settings.get("useFramebuffer") and settings.get("framebuffer"):
    #    os.environ["QT_QPA_PLATFORM"] = f'linuxfb:fb={settings["framebuffer"]}'

    webserver = None
    ip_port = None
    settings = parseSettings()

    def _networkCheck(splash: Startup):
        global ip_port

        splash.onNetworkCheck.emit()

        while not (ip_port := checkNetwork()):
            print("ERROR: network not available, retrying...")
            time.sleep(1)

        time.sleep(1)

        splash.onFinish.emit()

    app = QApplication(sys.argv)
    print(app.platformName())

    splash = Startup()
    Thread(target=_networkCheck, args=(splash,)).start()
    splash.exec()

    player = Player(ip_port)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", player)
    engine.quit.connect(app.quit)
    engine.load(QML)

    if not engine.rootObjects():
        sys.exit(1)

    if settings.get("runWebserver"):
        print(f"starting HTTP server on: {ip_port[0]}:{ip_port[1]}")

        webserver = server.initServer(ip_port, SETTINGS, STATIONS)
        webserverThread = Thread(target=webserver.serve_forever)
        webserverThread.start()

        print("webserver started")

    else:
        player.setWebserverUrl( *("webserver disabled", "") )

    if settings.get("autotimer"):
        player.setAutoTimer(True)

    def close(*args, **kwargs):
        print("exit triggered")
        app.exit(0)

    signal.signal(signal.SIGINT, close)
    signal.signal(signal.SIGTERM, close)

    exitcode = app.exec_()
    
    if webserver and webserverThread:
        print("stopping webserver")
        webserver.shutdown()
        webserverThread.join()

    sys.exit(exitcode)
