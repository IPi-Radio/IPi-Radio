# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '1024x600_v2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("QGroupBox {\n"
"    border: 4px solid rgb(255, 255, 255);\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_status = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy)
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setObjectName("label_status")
        self.verticalLayout_2.addWidget(self.label_status)
        self.label_radioname = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_radioname.sizePolicy().hasHeightForWidth())
        self.label_radioname.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label_radioname.setFont(font)
        self.label_radioname.setAlignment(QtCore.Qt.AlignCenter)
        self.label_radioname.setObjectName("label_radioname")
        self.verticalLayout_2.addWidget(self.label_radioname)
        self.label_time = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_time.sizePolicy().hasHeightForWidth())
        self.label_time.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(31)
        self.label_time.setFont(font)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setObjectName("label_time")
        self.verticalLayout_2.addWidget(self.label_time)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.button_stop = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_stop.sizePolicy().hasHeightForWidth())
        self.button_stop.setSizePolicy(sizePolicy)
        self.button_stop.setBaseSize(QtCore.QSize(0, 70))
        self.button_stop.setObjectName("button_stop")
        self.gridLayout.addWidget(self.button_stop, 0, 1, 1, 1)
        self.button_auto = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_auto.sizePolicy().hasHeightForWidth())
        self.button_auto.setSizePolicy(sizePolicy)
        self.button_auto.setObjectName("button_auto")
        self.gridLayout.addWidget(self.button_auto, 1, 1, 1, 1)
        self.button_reboot = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_reboot.sizePolicy().hasHeightForWidth())
        self.button_reboot.setSizePolicy(sizePolicy)
        self.button_reboot.setBaseSize(QtCore.QSize(0, 70))
        self.button_reboot.setStyleSheet("color: rgb(140, 140, 255);")
        self.button_reboot.setObjectName("button_reboot")
        self.gridLayout.addWidget(self.button_reboot, 0, 0, 1, 1)
        self.button_shutdown = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_shutdown.sizePolicy().hasHeightForWidth())
        self.button_shutdown.setSizePolicy(sizePolicy)
        self.button_shutdown.setStyleSheet("color: rgb(255, 140, 140);")
        self.button_shutdown.setObjectName("button_shutdown")
        self.gridLayout.addWidget(self.button_shutdown, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.radiolist = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radiolist.sizePolicy().hasHeightForWidth())
        self.radiolist.setSizePolicy(sizePolicy)
        self.radiolist.setFocusPolicy(QtCore.Qt.NoFocus)
        self.radiolist.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.radiolist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.radiolist.setProperty("showDropIndicator", False)
        self.radiolist.setObjectName("radiolist")
        self.horizontalLayout.addWidget(self.radiolist)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.button_shutdown.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "v1.1"))
        self.label_status.setText(_translate("MainWindow", "Status: unknown"))
        self.label_radioname.setText(_translate("MainWindow", "Radio Station"))
        self.label_time.setText(_translate("MainWindow", "00:00:00"))
        self.button_stop.setText(_translate("MainWindow", "STOP"))
        self.button_auto.setText(_translate("MainWindow", "AUTO: ON"))
        self.button_reboot.setText(_translate("MainWindow", "Reboot"))
        self.button_shutdown.setText(_translate("MainWindow", "Shutdown"))

