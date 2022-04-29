#! /usr/bin/env python3

from PyQt5.QtGui import ( 
    QStandardItem, QStandardItemModel
)

from PyQt5.QtCore import (
    Qt, QObject, 
    pyqtSignal, pyqtSlot, pyqtProperty
)

from constants import VERSION

DEFAULT_STR = "---"

class RadioListModel(QStandardItemModel):

    def __init__(self):
        super().__init__()

        self.radioName_r = Qt.UserRole
        self.timeFrames_r = Qt.UserRole + 1
        self.timeEnabled_r = Qt.UserRole + 2

        self.setItemRoleNames({
            self.radioName_r: b"radio_name",
            self.timeFrames_r: b"time_frames",
            self.timeEnabled_r: b"time_enabled",
        })

    def addItem(self, radioName, timeFrames="", timeEnabled=False):
        item = QStandardItem()
        item.setData(radioName, self.radioName_r)
        item.setData(timeEnabled, self.timeEnabled_r)
        item.setData(timeFrames, self.timeFrames_r)
        
        self.appendRow(item)


class Controller(QObject):
    pushMessage = pyqtSignal(str)
    triggerQuit = pyqtSignal()

    version_text_changed = pyqtSignal()
    status_text_changed = pyqtSignal()
    radio_name_changed = pyqtSignal()
    dls_text_changed = pyqtSignal()
    clock_changed = pyqtSignal()
    codec_text_changed = pyqtSignal()
    country_text_changed = pyqtSignal()
    web_url_addr_changed = pyqtSignal()

    auto_timer_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.radioList = RadioListModel()
        
        self.resetRadioInfo(True)
        self.setVersion(VERSION)

        self.setAutoTimer(False)

    def resetRadioInfo(self, all=False):
        self.setDLS(DEFAULT_STR)
        self.setCodec(DEFAULT_STR)
        self.setCountry(DEFAULT_STR)
        self.setRadioName("IPi-Radio")

        if all:
            self.setClock("00:00:00")
            self.setWebUrl(DEFAULT_STR)
            self.setStatusText(DEFAULT_STR)

    ## setters

    def setVersion(self, text: str):
        self._version_text = f"v{text}"
        self.version_text_changed.emit()

    def setStatusText(self, text: str):
        self._status_text = text
        self.status_text_changed.emit()

    def setRadioName(self, text: str):
        self._radio_name = text
        self.radio_name_changed.emit()

    def setDLS(self, text: str):
        self._dls_text = text
        self.dls_text_changed.emit()

    def setClock(self, text: str):
        self._clock = text
        self.clock_changed.emit()

    def setCodec(self, text: str):
        self._codec_text = text
        self.codec_text_changed.emit()

    def setCountry(self, text: str):
        self._country_text = text
        self.country_text_changed.emit()

    def setWebUrl(self, text: str):
        self._web_url_addr = text
        self.web_url_addr_changed.emit()

    def setAutoTimer(self, state: bool):
        self._auto_timer = state
        self.auto_timer_changed.emit()

    ## functions

    ## properties

    @pyqtProperty(str, notify=version_text_changed)
    def version_text(self):
        return self._version_text

    @pyqtProperty(str, notify=status_text_changed)
    def status_text(self):
        return self._status_text

    @pyqtProperty(str, notify=radio_name_changed)
    def radio_name(self):
        return self._radio_name

    @pyqtProperty(str, notify=dls_text_changed)
    def dls_text(self):
        return self._dls_text

    @pyqtProperty(str, notify=clock_changed)
    def clock(self):
        return self._clock

    @pyqtProperty(str, notify=codec_text_changed)
    def codec_text(self):
        return self._codec_text

    @pyqtProperty(str, notify=country_text_changed)
    def country_text(self):
        return self._country_text

    @pyqtProperty(str, notify=web_url_addr_changed)
    def web_url_addr(self):
        return self._web_url_addr

    @pyqtProperty(QObject, constant=True)
    def list_model(self):
        return self.radioList

    @pyqtProperty(bool, fset=setAutoTimer, notify=auto_timer_changed)
    def auto_timer(self):
        return self._auto_timer