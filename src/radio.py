#! /usr/bin/env python3

import re
import json
import urllib.request
import subprocess

from collections import OrderedDict
from datetime import datetime, timedelta

from PyQt5.QtCore import (
    QTimer, 
    QTime, 
    QUrl,
    pyqtSlot
)
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from constants import VERSION, VERSION_URL, STATIONS, ICON, SELECTION_TIMEOUT
from ui.GuiController import Controller

"""
screen res:
1024x600

480x320
"""

class Player(Controller):
    def __init__(self):
        super().__init__()

        self.currStation = None
        self.radioStations = OrderedDict()

        # mediaplayer
        self.player = QMediaPlayer(self, QMediaPlayer.Flag.StreamPlayback)
        self.player.metaDataChanged.connect(self._updateMetadata)

        # setup UI
        #self.setRadioIcon(False)
        self.readRadioList()

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
    def stopRadio(self, resetTimer=True):
        if resetTimer: self.setAutoTimer(False)

        self.player.stop()

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

            # this causes issues with currentIndex, highlightItem etc crap being NULL
            #self.radioList.clear()
            self.radioList.setRowCount(0)

            #print(list(self.radioStations.items()))
            for _, (key, value) in enumerate(self.radioStations.items()):
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
        print("SET RADIO")
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

        self.player.setMedia(QMediaContent(QUrl(station.get("url"))))
        self.player.play()

        ## TODO: run this in a separate thread to avoid blocking
        #self.setRadioIcon(data=station.get("favicon"), isURL=True)

        # this HAS to run before the timer, otherwise you get infinite loop!
        self.currStation = stationName 

        self._timer()

    def setWebserverUrl(self, ip: str, port: str):
        if port:
            self.setWebUrl(f"{ip}:{port}")
        else:
            self.setWebUrl(ip)

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
                self.stopRadio(False)

    def _timer(self):
        self.setClock( QTime.currentTime().toString("hh:mm:ss") )

        stateText = ""

        # set player state
        state = self.player.state()
        if state == QMediaPlayer.State.StoppedState:
            stateText = "stopped"

        elif state == QMediaPlayer.State.PausedState:
            stateText = "paused"

        elif state == QMediaPlayer.State.PlayingState:
            stateText = "playing"

        else:
            stateText = "unknown"

        if self.player.error() != QMediaPlayer.Error.NoError:
            stateText = self.player.errorString()

        self.setStatusText(f"({self.player.mediaStatus()}) {stateText}")

        self._checkRadioStation()

    def _updateMetadata(self):
        if not self.player.isMetaDataAvailable():
            return
        
        #print("---")
        #for entry in self.player.availableMetaData():
        #    print(entry, ":", self.player.metaData(entry))

        if title := self.player.metaData("Title"):
            self.setDLS(title)
        
        if codec := self.player.metaData("AudioCodec"):
            if bitrate := self.player.metaData("AudioBitRate"):
                self.setCodec(f"{codec} ({int(bitrate)//1000} kbits)")
            else:
                self.setCodec(codec)

        #print("metadata updated")

    def updateCheck(self):
        """fetches version information from VERSION file on Github respository"""
        try:
            print("checking for updates...", end="")
            latestVersion = urllib.request.urlopen(VERSION_URL, timeout=1).read().decode().strip()
            installedVersion = VERSION

            if installedVersion < latestVersion:
                print(f"found new version {installedVersion} {latestVersion}")
                self.setVersion(f"{VERSION} (new version available)")
            else:
                print("latest version installed")
        except Exception as e:
            print("failed!")
            print(str(e))
