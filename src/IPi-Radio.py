#! /usr/bin/env python3

import os
import re
import sys
import json
import time
#import keyboard
import subprocess

import vlc

from collections import OrderedDict
from datetime import datetime, timedelta

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMessageBox

from gui import Ui_MainWindow

"""
screen res:
1024x600

480x320
"""

STATIONS = "stations.json"

class Player(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.currStation = None
        self.autoTimer = False
        self.volume = 100

        self.instance = vlc.Instance("--no-xlib")
        self.vlcPlayer: vlc.MediaPlayer = self.instance.media_player_new()

        self.setupUi(self)
        self.readRadioList()
        self.checkAutoTimer()

        #self.button_vol_plus.clicked.connect(self.add)
        #self.button_vol_minus.clicked.connect(self.sub)
        self.radiolist.itemClicked.connect(self.selectRadio)

        self.button_auto.clicked.connect(self.toggleAutoTimer)
        self.button_stop.clicked.connect(self.stopRadio)
        self.button_reboot.clicked.connect(self.reboot)
        self.button_shutdown.clicked.connect(self.shutdown)

        #self.button_test.clicked.connect(self.testfunction)

        # init clock
        timer_sec = QTimer(self)
        timer_sec.timeout.connect(self._timer)
        timer_sec.start(1000)

        # lambdas
        self.getStationName = lambda x: list(self.radioStations.items())[x][0]

    def readRadioList(self):
        """init the list of radio stations by reading from the json file"""
        with open(os.path.join(os.path.dirname(__file__), STATIONS), "r") as f:
            self.radioStations: OrderedDict = json.load(fp=f, object_pairs_hook=OrderedDict)

        print(list(self.radioStations.items()))
        for i, (key, value) in enumerate(self.radioStations.items()):
            #print(key, value)
            self.radiolist.addItem(f"({i+1}) {key}")

    def resetRadioInformation(self): # should get called, when pressing the STOP button
        """"resets all information of the current radio station"""
        pass

    def testfunction(self):
        self.showQuestionMSG("some cool message")

    # Messageboxes
    def showQuestionMSG(self, msg_str: str, title_msg="QUESTION"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        
        reply = msg.exec_()

        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def setRadio(self, stationName: str):
        station: dict = self.radioStations.get(stationName)
        self.label_info_codec.setText(station.get("codec"))
        self.label_info_country.setText(station.get("country"))
        self.label_info_language.setText(station.get("language"))

        self.label_radioname.setText(stationName)

        media: vlc.Media = self.instance.media_new( station.get("url") )

        self.vlcPlayer.set_media(media)
        self.vlcPlayer.play()
        self._timer()
        
        self.currStation = stationName

    def selectRadio(self, ev: QListWidgetItem):
        #print(ev.text())
        ev.setSelected(True)
        
        itemIndex = self.radiolist.currentRow()
        rName = self.getStationName(itemIndex)

        self.autoTimer = True
        self.toggleAutoTimer()

        self.setRadio(rName)

        self._blinkOff(ev, 1000)

    def _blinkOff(self, li: QListWidgetItem, initMilis: int):
        QTimer.singleShot(initMilis, lambda:li.setSelected(False))
        QTimer.singleShot(initMilis + 100, lambda:li.setSelected(True))
        QTimer.singleShot(initMilis + 300, lambda:li.setSelected(False))

    def stopRadio(self):
        self.vlcPlayer.stop()
        self.currStation = None
        self.label_radioname.setText("IPi-Radio")
        self.label_info_codec.setText("---")
        self.label_info_country.setText("---")
        self.label_info_language.setText("---")

    def add(self):
        if 0 <= self.volume+5 <= 100:
            self.volume += 5
            self.label_volume.setText(f"Volume: {self.volume}%")

    def sub(self):
        if 0 <= self.volume-5 <= 100:
            self.volume -= 5
            self.label_volume.setText(f"Volume: {self.volume}%")

    def _getTimeComponents(self, time: str):
        exactTime = re.compile(r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
        timeFrame = re.compile(r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9](\s-\s|-)([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")

        if exactTime.match(time):
            timeObjStart = datetime.strptime(time, '%H:%M')
            timeObjEnd = timeObjStart + timedelta(seconds=59)

            return timeObjStart.time(), timeObjEnd.time()
            
        elif timeFrame.match(time):
            time = time.replace(' ', '') # remove whitespace
            t1, t2 = time.split("-")

            timeObjStart = datetime.strptime(t1, '%H:%M')
            timeObjEnd = datetime.strptime(t2, '%H:%M')

            return timeObjStart.time(), timeObjEnd.time()
        else:
            # TODO: show error message
            return False, False

    def _timeInBetween(self, start, end):
        now = datetime.now().time()
        if start <= end:
            return start <= now <= end
        else: # over midnight e.g., 23:30-04:15
            return start <= now or now <= end

    def _checkRadioStation(self):
        if self.autoTimer:
            playing = False
            for key, value in self.radioStations.items():
                tTime = value["time"]
                if not tTime: continue

                if self._timeInBetween( *self._getTimeComponents(tTime) ):
                    playing = True
                    if self.currStation != key:
                        self.setRadio(key)
                    break

            if not playing and self.currStation:
                print("stop")
                self.stopRadio()

    def _timer(self):
        self.label_time.setText( QTime.currentTime().toString("hh:mm:ss") )

        state: vlc.State = self.vlcPlayer.get_state()
        self.label_status.setText(f"Status: {state.__str__().split('.')[-1]}")

        self._checkRadioStation()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        #print("key pressed", a0.key())

        key_pressed = a0.key() - Qt.Key_0
        print(key_pressed)

        if 1 <= key_pressed <= min(len(self.radioStations), 9):
            #rNameItem: QListWidgetItem = self.radiolist.item(key_pressed-1)
            rName = self.getStationName(key_pressed-1)
            print("playing", rName)

            self.setRadio(rName)
        elif key_pressed == 0:
            self.stopRadio()

        #return super().keyPressEvent(a0)

    def toggleAutoTimer(self):
        self.autoTimer = not self.autoTimer
        self.checkAutoTimer()

    def checkAutoTimer(self):
        if self.autoTimer:
            self.button_auto.setText("AUTO: ON")
        else:
            self.button_auto.setText("AUTO: OFF")

    def reboot(self):
        subprocess.run(["sudo", "reboot", "now"])

    def shutdown(self):
        subprocess.run(["sudo", "shutdown", "now"])

if __name__ == "__main__":

    # this is from https://doc.qt.io/qt-5/embedded-linux.html
    # run without X server
    #os.environ["QWS_DISPLAY"] = r"linuxfb:fb=/dev/fb0"
    os.environ["QT_QPA_PLATFORM"] = "linuxfb:fb=/dev/fb0"

    app = QApplication(sys.argv)

    window = Player()
    window.show()

    sys.exit(app.exec())
