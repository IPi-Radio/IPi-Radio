import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    id: mainWindow
    width: 800
    height: 450
    color: "#101010"
    focus: true

    Connections {
        target: controller
    }

    Rectangle {
        id: leftThird

        color: "#00ffffff"
        width: parent.width * 2/3
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0

        RadioInfo {
            id: radioInfo
            border.width: 5
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.topMargin: border.width
            anchors.rightMargin: border.width
            anchors.leftMargin: border.width

            anchors.bottom: buttonPanel.top
            anchors.bottomMargin: border.width * 3

            state: controller.auto_timer ? "auto" : "base"

            versionText: controller.version_text
            statusText: controller.status_text
            radioName: controller.radio_name
            dlsText: controller.dls_text
            clock: controller.clock
            codecText: controller.codec_text
            countryText: controller.country_text
            webAddress: controller.web_url_addr
        }

        Grid {
            id: buttonPanel

            property int gridPadding: parent.width * 0.05

            rows: 2
            rowSpacing: 8
            columns: 3
            columnSpacing: gridPadding
            leftPadding: gridPadding
            rightPadding: leftPadding

            //property int buttonWidth: Math.min(250, width/2 - padding*4)
            property int buttonWidth: 200
            property int buttonHeight: 60
            property int textSize: 12
            property int borderWidth: 5
            property int radius: 10

            //anchors.top: radioInfo.bottom
            anchors.bottom: parent.bottom
            layoutDirection: Qt.RightToLeft
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: radioInfo.border.width * 2
            anchors.topMargin: radioInfo.border.width * 2

            CButton {
                id: stopBtn
                text: "STOP"
                textSize: buttonPanel.textSize
                width: buttonPanel.buttonWidth
                height: buttonPanel.buttonHeight
                border.width: buttonPanel.borderWidth
                radius: buttonPanel.radius

                indicatorSize: 25

                onClicked: controller.stopRadio();
            }
            CButton {
                id: shutdownBtn
                text: "Shutdown"

                textSize: buttonPanel.textSize
                textColor: "#ff8e8c"

                width: 125
                height: buttonPanel.buttonHeight
                border.width: buttonPanel.borderWidth
                radius: buttonPanel.radius
                indicatorEnabled: false

                onClicked: controller.shutdown()
            }
            CButton {
                id: rebootBtn
                text: "Reboot"

                textSize: buttonPanel.textSize
                textColor: "#8c8eff"

                width: 125
                height: buttonPanel.buttonHeight
                border.width: buttonPanel.borderWidth
                radius: buttonPanel.radius
                indicatorEnabled: false

                onClicked: controller.reboot()
            }
            CButton {
                id: autoBtn
                text: controller.auto_timer ? "AUTO: ON" : "AUTO: OFF"
                textSize: buttonPanel.textSize

                width: buttonPanel.buttonWidth
                height: buttonPanel.buttonHeight
                border.width: buttonPanel.borderWidth
                radius: buttonPanel.radius

                indicatorEnabled: false
                altMode: controller.auto_timer

                //onClicked: mainWindow.autoEnabled = !mainWindow.autoEnabled
                onClicked: controller.auto_timer = !controller.auto_timer
            }
        }
    }

    Rectangle {
        id: rightThird

        color: "#00ffffff"
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.topMargin: 0
        anchors.bottomMargin: 0
        anchors.rightMargin: 0
        width: parent.width * 1/3


        ScrollView {
            anchors.fill: parent

            ListView {
                id: radioList
                anchors.fill: parent

                model: controller.list_model
                delegate: listViewDelegate
                highlight: highlightDelegate
                highlightFollowsCurrentItem: true
                highlightMoveDuration: 250

                onCurrentIndexChanged: {
                    updateTimer();
                }
            }
        }
    }

    Component {
        id: listViewDelegate

        ListEntry {
            indicatorKey: index+1
            radioName: radio_name
            timeFrames: time_frames
            timeEnabled: time_enabled
            width: parent.width - radioList.highlightItem.border.width

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onContainsMouseChanged: {
                    radioList.currentIndex = index;
                }
                onClicked: {
                    controller.selectRadio(index, parent.radioName);
                }

                onPressed: {
                    radioList.highlightItem.state = "pressed"
                }
                onReleased: {
                    if (containsMouse)
                        radioList.highlightItem.state = "base"
                    else
                        radioList.highlightItem.state = "base"
                }
            }
        }
    }

    Component {
        id: highlightDelegate
        Rectangle {
            id: highlightRect
            property alias timer: highlightTimer

            radius: 20
            color: "#00ffffff"
            opacity: 1
            border.width: 5
            border.color: "lightsteelblue"

            Behavior on opacity {
                NumberAnimation {
                    duration: 1000
                }
            }
            Behavior on border.color {
                ColorAnimation {
                    duration: 100
                }
            }

            Timer {
                id: highlightTimer
                interval: 5*1000
                repeat: false
                triggeredOnStart: false
                onTriggered: {
                    console.log("timer trigger");
                    parent.opacity = 0;
                }
            }

            state: "base"
            states: [
                State {
                    name: "base"
                    PropertyChanges {
                        target: highlightRect
                        border.color: "lightsteelblue"
                    }
                },
                State {
                    name: "pressed"
                    PropertyChanges {
                        target: highlightRect
                        border.color: "white"
                    }
                }
            ]
        }
    }

    Timer {
        id: timer
        function setTimeout(cb, delayTime) {
            timer.interval = delayTime;
            timer.repeat = false;
            timer.triggered.connect(cb);
            timer.triggered.connect(function release() {
                timer.triggered.disconnect(cb);
                timer.triggered.disconnect(release);
            });
            timer.start();
            console.log("timer started");
        }
    }

    property bool inListSelected: true
    property int horSelection: 0
    property int vertSelection: 0
    property var btnMapping: [
        btnMappingUpper, btnMappingLower
    ]
    property var btnMappingUpper: [
        rebootBtn,
        shutdownBtn,
        stopBtn
    ]
    property var btnMappingLower: [
        autoBtn
    ]

    function updateTimer() {
        let hItem = radioList.highlightItem;

        hItem.opacity = 1;
        if (hItem.timer.running)
            hItem.timer.restart();
        else
            hItem.timer.start();
    }
    function updateSelector() {

    }

    function selDown() {
        if (radioList.currentIndex >= 0) {
            if (radioList.currentIndex + 1 >= radioList.count)
                updateTimer();
            else
                radioList.currentIndex += 1;
        }


    }
    function selUp() {
        if (radioList.currentIndex >= 0) {
            if (radioList.currentIndex <= 0)
                updateTimer();
            else
                radioList.currentIndex -= 1;
        }


    }

    function selLeft() {
        if (inListSelected) {
            inListSelected = false;
            horSelection = 0;
            vertSelection = 0;
        }
    }
    function selRight() {

    }

    Keys.onPressed: {
        let key = event.key;

        if (key === Qt.Key_0)
            stopBtn.clicked();

        key = key - Qt.Key_0 - 1;

        if (0 <= key && key < radioList.count) {
            updateTimer();
            radioList.currentIndex = key;
            controller.selectRadio(key, radioList.currentItem.radioName);
        }

        if (event.key === 16777360) // Home button
            autoBtn.clicked();

        //if (event.key === 16777219) // backspace
        //    shutdownBtn.clicked();

        console.log(event.key);
    }

    Keys.onDownPressed: {
        selDown();
    }
    Keys.onUpPressed: {
        selUp();
    }
    Keys.onLeftPressed: {
        // TODO
        //selLeft();
    }
    Keys.onRightPressed: {
        // TODO
        //selRight();
    }

    Keys.onReturnPressed: {
        controller.selectRadio(radioList.currentIndex, radioList.currentItem.radioName);
        updateTimer();
    }

    Keys.onEscapePressed: {
        Qt.quit();
    }
}
