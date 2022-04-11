#! /usr/bin/env python3

import os
import re
import sys
import json
import socket
import urllib.request
import subprocess

import vlc

from collections import OrderedDict
from datetime import datetime, timedelta

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, Qt, QTime, pyqtSlot
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

from constants import VERSION, VERSION_URL, STATIONS, ICON, SELECTION_TIMEOUT
from ui.GuiController import Controller

"""
screen res:
1024x600

480x320
"""

class Player(Controller):
    def __init__(self, ip_port: tuple):
        super().__init__()

        self.currStation = None
        self.radioStations = OrderedDict()

        # create VLC instance
        self.instance: vlc.Instance = vlc.Instance("--no-xlib")
        self.vlcPlayer: vlc.MediaPlayer = self.instance.media_player_new()

        # setup UI
        #self.setRadioIcon(False)
        self.readRadioList()
        self.setWebUrl(f"{ip_port[0]}:{ip_port[1]}")

        # init clock
        timer_sec = QTimer(self)
        timer_sec.timeout.connect(self._timer)
        timer_sec.start(1000)

        # timer for updating the radio list
        timer_listupdate = QTimer(self)
        timer_listupdate.timeout.connect(self.readRadioList)
        timer_listupdate.start(10 * 1000)

        # timer for the update check
        timer_updatecheck = QTimer(self)
        timer_updatecheck.timeout.connect(self.updateCheck)
        self.updateCheck()
        timer_updatecheck.start(3600 * 1000)

        # lambdas
        self.getStationName = lambda x: list(self.radioStations.items())[x][0]

    ## QT SLOTS

    @pyqtSlot(int, str)
    def selectRadio(self, index: int, radioName: str):
        print(index, radioName)

        self.setAutoTimer(False)
        self.setRadio(radioName)

    @pyqtSlot()
    def stopRadio(self):
        self.setAutoTimer(False)
        self.vlcPlayer.stop()
        self.currStation = None
        self.resetRadioInfo()

    @pyqtSlot()
    def reboot(self):
        subprocess.run(["sudo", "reboot", "now"])

    @pyqtSlot()
    def shutdown(self):
        subprocess.run(["sudo", "shutdown", "now"])

    ##

    def readRadioList(self):
        """init the list of radio stations by reading from the json file"""

        try:
            with open(STATIONS, "r") as f:
                stationData: OrderedDict = json.load(fp=f, object_pairs_hook=OrderedDict)
        except FileNotFoundError:
            print(f"WARNING: Could not find stations file: {STATIONS}")
            print("generating new empty one...")

            with open(STATIONS, "w") as f:
                f.write("{}")
            return

        # only update UI when there are changes
        if stationData != self.radioStations:
            self.radioStations = stationData

            self.radioList.clear()

            #print(list(self.radioStations.items()))
            for i, (key, value) in enumerate(self.radioStations.items()):
                #print(key, value)
                if value.get("time"):
                    self.radioList.addItem(
                        radioName=key, 
                        timeFrames=value["time"], timeEnabled=True)
                else:
                    self.radioList.addItem(radioName=key)

            print("radio list updated!")

#    def setRadioIcon(self, isURL: bool, data=None):
#        if isURL:
#            try:
#                rIcon_data = urllib.request.urlopen(data, timeout=1).read()
#                rPixmap = QtGui.QPixmap()
#                rPixmap.loadFromData(rIcon_data)
#                rPixmap = rPixmap.scaledToHeight(32)
#
#                print("set ICON")
#                self.label_radio_icon.setPixmap(rPixmap)
#            except:
#                print("clear ICON")
#                self.label_radio_icon.clear()
#        else:
#            self.label_radio_icon.setPixmap( QtGui.QPixmap(ICON) )
            

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
        self.resetRadioInfo()

        station: dict = self.radioStations.get(stationName)
        if station.get("bitrate") > 0:
            self.setCodec(f'{station.get("codec")} ({station.get("bitrate")} kbps)')
        else:
            self.setCodec(station.get("codec"))

        self.setCountry(f'{station.get("countrycode")} {station.get("language")}')

        # set radio name and image
        #if len(stationName) >= 20:
        #    tstationName = stationName[:30]
        #else:
        #    tstationName = stationName
        
        self.setRadioName(stationName)

        media: vlc.Media = self.instance.media_new( station.get("url") )
        media.get_mrl()

        self.vlcPlayer.set_media(media)
        self.vlcPlayer.play()

        ## TODO: run this in a separate thread to avoid blocking
        #self.setRadioIcon(data=station.get("favicon"), isURL=True)

        # this HAS to run before the timer, otherwise you get infinite loop!
        self.currStation = stationName 

        self._timer()

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
        #print("timer: ", self.auto_timer)
        if self.auto_timer:
            playing = False
            for key, value in self.radioStations.items():
                tTime = value["time"]
                if not tTime or tTime == "default":
                    continue

                if self._timeInBetween( *self._getTimeComponents(tTime) ):
                    playing = True
                    if self.currStation != key:
                        self.setRadio(key)
                    break

            # run second loop for checking default radio station
            if not playing:
                for key, value in self.radioStations.items():
                    if value["time"] == "default":
                        playing = True
                        if self.currStation != key:
                            self.setRadio(key)
                        break

            if not playing and self.currStation:
                print("stop")
                self.stopRadio()

    def _timer(self):
        self.setClock( QTime.currentTime().toString("hh:mm:ss") )

        # set VLC state
        state: vlc.State = self.vlcPlayer.get_state()
        self.setStatusText( str(state.__str__().split('.')[-1]) )

        # set DLS from stream metadata
        if self.vlcPlayer.is_playing() == 1 and self.currStation:
            media: vlc.Media = self.vlcPlayer.get_media()
            if media:
                media.parse_with_options(vlc.MediaParseFlag(0), 500)
                radioDLS: str = media.get_meta(12)

                if self.dls_text != radioDLS and radioDLS:
                    self.setDLS(radioDLS)
                elif not radioDLS:
                    self.setDLS("no DLS")

        self._checkRadioStation()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        #print("key pressed", a0.key())

        key_pressed = a0.key() - Qt.Key_0
        #print(key_pressed)

        if 1 <= key_pressed <= min(len(self.radioStations), 9):
            #rNameItem: QListWidgetItem = self.radiolist.item(key_pressed-1)
            rName = self.getStationName(key_pressed-1)
            print("playing", rName)
            self.setAutoTimer(False)

            self.setRadio(rName)

        elif key_pressed == 0x0:
            self.button_stop.click()
            #self.stopRadio()

        elif key_pressed == 0xFFFFE5: # UP button
            self.selectDown()
        elif key_pressed == 0xFFFFE3: # DOWN button
            self.selectUp()

        elif key_pressed == 0xFFFFD4: # ENTER button
            cItem = self.radiolist.currentItem()
            if cItem:
                self.selectRadio(cItem)

        #return super().keyPressEvent(a0)


    def updateCheck(self):
        # version check
        try:
            print("checking for updates...", end="")
            latestVersion = float(urllib.request.urlopen(VERSION_URL, timeout=1).read())
            installedVersion = float(VERSION)

            if installedVersion < latestVersion:
                print("found new version")
                self.groupBox.setTitle(f"v{installedVersion} (new version available)")
            else:
                print("latest version installed")
        except:
            print("failed!")
