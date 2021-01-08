import os
import sys
import json
import time
#import keyboard
import subprocess

import vlc

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem

from gui import Ui_MainWindow

"""
screen res:
1024x600

480x320
"""


class Player(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.currStation = None
        self.autoTimer = True
        self.volume = 100

        self.instance = vlc.Instance("--no-xlib")
        self.vlcPlayer: vlc.MediaPlayer = self.instance.media_player_new()

        self.setupUi(self)
        self.initRadioList()

        #self.button_vol_plus.clicked.connect(self.add)
        #self.button_vol_minus.clicked.connect(self.sub)
        self.radiolist.itemClicked.connect(self.selectRadio)

        self.button_auto.clicked.connect(self.toggleAutoTimer)
        self.button_stop.clicked.connect(self.stopRadio)
        self.button_reboot.clicked.connect(self.reboot)
        self.button_shutdown.clicked.connect(self.shutdown)

        # init clock
        timer_sec = QTimer(self)
        timer_sec.timeout.connect(self._timer)
        timer_sec.start(1000)

    def initRadioList(self):
        with open(os.path.join(os.path.dirname(__file__), "radiostations.json"), "r") as f:
            self.radioStations: dict = json.load(fp=f)

        #print(self.radioStations)
        for key, value in self.radioStations.items():
            print(key, value)
            self.radiolist.addItem(key)


    def setRadio(self, stationName: str):
        self.label_radioname.setText(stationName)
        
        media: vlc.Media = self.instance.media_new( self.radioStations.get(stationName) )

        self.vlcPlayer.set_media(media)
        self.vlcPlayer.play()

        self.currStation = stationName

    def selectRadio(self, ev: QListWidgetItem):
        #print(ev.text())
        stationName = ev.text()

        self.label_radioname.setText(stationName)
        
        media: vlc.Media = self.instance.media_new(self.radioStations.get(stationName))

        self.vlcPlayer.set_media(media)
        self.vlcPlayer.play()

        self._timer()
        ev.setSelected(False)
        self.currStation = stationName
        self.autoTimer = True
        self.toggleAutoTimer()

    def stopRadio(self):
        self.vlcPlayer.stop()


    def add(self):
        if 0 <= self.volume+5 <= 100:
            self.volume += 5
            self.label_volume.setText(f"Volume: {self.volume}%")

    def sub(self):
        if 0 <= self.volume-5 <= 100:
            self.volume -= 5
            self.label_volume.setText(f"Volume: {self.volume}%")

    def _checkRadioStation(self):
        if self.autoTimer:
            currTime = QTime.currentTime().toString("hh")

            if currTime == "20":
                newStation = "Radio Vatikan"
            elif currTime == "21":
                newStation = "Bayern 5 plus"
            elif currTime == "15":
                newStation = "Radio Maria Schweiz"
            else:
                newStation = self.currStation

            if self.currStation != newStation:
                self.setRadio(newStation)

    def _timer(self):
        self.label_time.setText( QTime.currentTime().toString("hh:mm:ss") )

        state: vlc.State = self.vlcPlayer.get_state()
        self.label_status.setText(f"Status: {state.__str__().split('.')[-1]}")

        self._checkRadioStation()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        #print("key pressed", a0.key())

        key_pressed = a0.key() - Qt.Key_1
        #print(key_pressed)

        if 0 <= key_pressed < len(self.radioStations):
            rNameItem: QListWidgetItem = self.radiolist.item(key_pressed)
            print("playing", rNameItem.text())

            if self.radioStations.get(rNameItem.text()):
                print(rNameItem.text())
                rNameItem.setSelected(True)
                self.selectRadio(rNameItem)

        #return super().keyPressEvent(a0)

    def toggleAutoTimer(self):
        if self.autoTimer:
            self.button_auto.setText("AUTO: OFF")
        else:
            self.button_auto.setText("AUTO: ON")
        
        self.autoTimer = not self.autoTimer

    def reboot(self):
        subprocess.run(["sudo", "reboot", "now"])

    def shutdown(self):
        subprocess.run(["sudo", "shutdown", "now"])

if __name__ == "__main__":

    # this is from https://doc.qt.io/qt-5/embedded-linux.html
    # run without X server
    #os.environ["QWS_DISPLAY"] = r"linuxfb:fb=/dev/fb0"
    os.environ["QT_QPA_PLATFORM"] = "linuxfb:fb=/dev/fb0"

    #gui = uic.loadUi("1024x600.ui")

    app = QApplication(sys.argv)

    window = Player()
    window.show()

    sys.exit(app.exec())
