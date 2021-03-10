#! /usr/bin/env python3

import os
import re
import sys
import json
import socket
import urllib.request
import subprocess

import vlc

from multiprocessing import Process
from collections import OrderedDict
from datetime import datetime, timedelta

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, Qt, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMessageBox, QStyleFactory

import server
from ui.gui import Ui_MainWindow

"""
screen res:
1024x600

480x320
"""

curr_location = os.path.dirname(os.path.realpath(__file__))
getAbsPath = lambda x, y: os.path.join(curr_location, x, y)

STATIONS = getAbsPath("settings", "stations.json")
SETTINGS = getAbsPath("settings", "settings.json")
ICON = getAbsPath("lib", "favicon.png")

SELECTION_TIMEOUT = 5*1000

VERSION_URL = "https://raw.githubusercontent.com/IPi-Radio/IPi-Radio/master/VERSION"

class Player(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.currStation = None
        self.radioStations = OrderedDict()

        self.currListItem = 0
        self.autoTimer = False
        self.volume = 100

        # create VLC instance
        self.instance = vlc.Instance("--no-xlib")
        self.vlcPlayer: vlc.MediaPlayer = self.instance.media_player_new()

        # setup UI
        self.setupUi(self)
        self.setRadioIcon(False)
        self.readRadioList()
        self.checkAutoTimer()
        self.label_info_IP.setText(f"{ip_port[0]}:{ip_port[1]}")

        #self.button_vol_plus.clicked.connect(self.add)
        #self.button_vol_minus.clicked.connect(self.sub)
        self.radiolist.itemClicked.connect(self.selectRadio)

        self.button_auto.clicked.connect(lambda: self.setAutoTimer(None))
        self.button_stop.clicked.connect(self.stopRadio)
        self.button_reboot.clicked.connect(self.reboot)
        self.button_shutdown.clicked.connect(self.shutdown)

        #self.button_test.clicked.connect(self.testfunction)

        # init clock
        timer_sec = QTimer(self)
        timer_sec.timeout.connect(self._timer)
        timer_sec.start(1000)

        # timer for selecting timeout
        self.timer_selection = QTimer(self)
        self.timer_selection.timeout.connect(self.disableSelection)

        # timer for updating the radio list
        timer_listupdate = QTimer(self)
        timer_listupdate.timeout.connect(self.readRadioList)
        timer_listupdate.start(10 * 1000)

        timer_updatecheck = QTimer(self)
        timer_updatecheck.timeout.connect(self.updateCheck)
        self.updateCheck()
        timer_updatecheck.start(3600 * 1000)

        # lambdas
        self.getStationName = lambda x: list(self.radioStations.items())[x][0]

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

            self.radiolist.clear()
            #print(list(self.radioStations.items()))
            for i, (key, value) in enumerate(self.radioStations.items()):
                #print(key, value)
                if value.get("time"):
                    self.radiolist.addItem(f'({i+1}) {key} \n time: ({value["time"]})')
                else:
                    self.radiolist.addItem(f'({i+1}) {key}')

            print("radio list updated!")

    def resetRadioInformation(self): # should get called, when pressing the STOP button
        """"resets all information of the current radio station"""
        self.label_radioname.setAlignment(Qt.AlignCenter)
        self.label_radioname.setText("IPi-Radio")
        self.setRadioIcon(False)
        self.label_info_codec.setText("---")
        self.label_info_country.setText("---")
        self.label_info_dls.setText("---")

    def setRadioIcon(self, isURL: bool, data=None):
        if isURL:
            try:
                rIcon_data = urllib.request.urlopen(data, timeout=1).read()
                rPixmap = QtGui.QPixmap()
                rPixmap.loadFromData(rIcon_data)
                rPixmap = rPixmap.scaledToHeight(32)

                print("set ICON")
                self.label_radio_icon.setPixmap(rPixmap)
            except:
                print("clear ICON")
                self.label_radio_icon.clear()
        else:
            self.label_radio_icon.setPixmap( QtGui.QPixmap(ICON) )
            

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
        self.resetRadioInformation()
        station: dict = self.radioStations.get(stationName)
        if station.get("bitrate") > 0:
            self.label_info_codec.setText(f'{station.get("codec")} ({station.get("bitrate")} kbps)')    
        else:
            self.label_info_codec.setText(station.get("codec"))
        self.label_info_country.setText(f'{station.get("countrycode")} {station.get("language")}')

        # set radio name and image
        if len(stationName) >= 20:
            tstationName = stationName[:30]
            self.label_radioname.setAlignment(Qt.AlignLeft)
        else:
            tstationName = stationName
            self.label_radioname.setAlignment(Qt.AlignCenter)
        self.label_radioname.setText(tstationName)

        media: vlc.Media = self.instance.media_new( station.get("url") )
        media.get_mrl()

        self.vlcPlayer.set_media(media)
        self.vlcPlayer.play()

        # TODO: run this in a separate thread to avoid blocking
        self.setRadioIcon(data=station.get("favicon"), isURL=True)

        self.currStation = stationName # this HAS to run before the timer, otherwise you get infinite loop!

        self._timer()

    def selectRadio(self, ev: QListWidgetItem):
        #print(ev.text())
        ev.setSelected(True)
        
        itemIndex = self.radiolist.currentRow()
        self.currListItem = itemIndex
        rName = self.getStationName(itemIndex)

        self.setAutoTimer(False)

        self.setRadio(rName)

        self._blinkOff(ev, 200)

    def _blinkOff(self, li: QListWidgetItem, initMilis: int):
        QTimer.singleShot(initMilis, lambda:li.setSelected(False))
        QTimer.singleShot(initMilis + 100, lambda:li.setSelected(True))
        QTimer.singleShot(initMilis + 300, lambda:li.setSelected(False))
        QTimer.singleShot(initMilis + 300, self.disableSelection)

    def stopRadio(self):
        self.vlcPlayer.stop()
        self.currStation = None
        self.resetRadioInformation()

    def selectDown(self):
        currIndex = self.radiolist.currentRow()
        if currIndex < 0:
            self.radiolist.setCurrentRow(self.currListItem)
        else:
            if self.radiolist.item(self.currListItem+1):
                self.currListItem += 1
            else:
                self.currListItem = 0
            self.radiolist.setCurrentRow(self.currListItem)

        self._triggerSelectionTimer()

    def selectUp(self):
        currIndex = self.radiolist.currentRow()
        if currIndex < 0:
            self.radiolist.setCurrentRow(self.currListItem)
        else:
            if self.radiolist.item(self.currListItem-1):
                self.currListItem -= 1
            else:
                self.currListItem = len(self.radiolist)-1
            self.radiolist.setCurrentRow(self.currListItem)

        self._triggerSelectionTimer()

    def disableSelection(self):
        self.radiolist.setCurrentRow(-1)
        self.timer_selection.stop()

    def _triggerSelectionTimer(self):
        if not self.timer_selection.isActive():
            self.timer_selection.start(SELECTION_TIMEOUT)
        else:
            self.timer_selection.setInterval(SELECTION_TIMEOUT)

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
        self.label_time.setText( QTime.currentTime().toString("hh:mm:ss") )

        # set VLC state
        state: vlc.State = self.vlcPlayer.get_state()
        self.label_status.setText(f"Status: {state.__str__().split('.')[-1]}")

        # set DLS from stream metadata
        if self.vlcPlayer.is_playing() == 1 and self.currStation:
            media: vlc.Media = self.vlcPlayer.get_media()
            if media:
                media.parse_with_options(vlc.MediaParseFlag(0), 500)
                radioDLS: str = media.get_meta(12)

                if self.label_info_dls.text() != radioDLS and radioDLS:
                    self.label_info_dls.setText(radioDLS)
                elif not radioDLS:
                    self.label_info_dls.setText("no DLS")

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

    def setAutoTimer(self, state=None):
        if state != None:
            self.autoTimer = state
        else:
            self.autoTimer = not self.autoTimer
        
        self.checkAutoTimer()

    def checkAutoTimer(self):
        if self.autoTimer:
            self.button_auto.setText("AUTO: ON")
            self.groupBox.setStyleSheet("QGroupBox {border: 4px solid rgb(255, 100, 100)}")
        else:
            self.button_auto.setText("AUTO: OFF")
            self.groupBox.setStyleSheet("QGroupBox {border: 4px solid rgb(255, 255, 255)}")

    def updateCheck(self):
        # version check
        try:
            print("checking for updates...", end="")
            latestVersion = float(urllib.request.urlopen(VERSION_URL, timeout=1).read())
            installedVersion = float(self.groupBox.title()[1:])

            if installedVersion < latestVersion:
                print("found new version")
                self.groupBox.setTitle(f"v{installedVersion} (new version available)")
            else:
                print("latest version installed")
        except:
            pass

    def reboot(self):
        subprocess.run(["sudo", "reboot", "now"])

    def shutdown(self):
        subprocess.run(["sudo", "shutdown", "now"])

def parseSettings() -> dict:
    with open(SETTINGS, "r") as f:
        settings: dict = json.load(f)

    return settings

def checkNetwork():
    print("checking network connection...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("1.1.1.1", 80))
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

if __name__ == "__main__":
    global ip_port

    try:
        settings = parseSettings()
    except FileNotFoundError:
        print(f"Could not find settings file: {SETTINGS}")
        sys.exit()

    # this is from https://doc.qt.io/qt-5/embedded-linux.html
    # run without X server
    #os.environ["QWS_DISPLAY"] = r"linuxfb:fb=/dev/fb0"
    if settings.get("useFramebuffer") and settings.get("framebuffer"):
        os.environ["QT_QPA_PLATFORM"] = f'linuxfb:fb={settings["framebuffer"]}'

    # init webserver
    webserver = None
    if settings.get("runWebserver"):
        ip_port = checkNetwork()

        if ip_port:
            print(f"starting HTTP server on: {ip_port[0]}:{ip_port[1]}")

            webserver = Process(target=server.run, args=(ip_port,))
            webserver.start()
            print("webserver started")
        else:
            print("ERROR: network not available!")
            sys.exit()
    else:
        ip_port = ("webserver disabled", "")

    app = QApplication(sys.argv)

    if settings.get("touchOptimize"):
        app.setStyle("bb10dark")
    else:
        app.setStyle("kvantum-dark")

    #print(app.style().metaObject().className()) # returns QBB10DarkStyle or bb10dark
    #print("available styles: ", QStyleFactory.keys())

    window = Player()
    window.show()

    # set autoTimer
    if settings.get("autotimer"):
        window.setAutoTimer(bool(settings["autotimer"]))

    # handle exit
    exitcode = app.exec()
    if webserver != None:
        print("stopping webserver...")
        webserver.terminate()

    sys.exit(exitcode)
