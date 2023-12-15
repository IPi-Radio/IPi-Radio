import QtQuick 2.12
import QtQuick.Controls 2.12

Item {
    id: listEntry
    width: 250
    height: 80

    property int margins: 8

    property alias indicatorKey: indicatorBox.text
    property alias indicatorColor: indicatorBox.color
    property color textColor: "white"

    property alias radioName: radio.text
    property alias timeFrames: timeFrame.text
    property bool timeEnabled: true

    property color separatorColor: "white"

    Rectangle {
        id: background
        color: "#404040"
        opacity: 0
        radius: 20

        anchors.fill: parent
        anchors.margins: listEntry.margins / 2

        Behavior on opacity {
            NumberAnimation {
                duration: 250
            }
        }
    }

    KeyIndicator {
        id: indicatorBox

        width: 25
        height: width

        anchors {
            left: parent.left
            leftMargin: listEntry.margins
            verticalCenter: parent.verticalCenter
        }

        color: "#000000ff"
        textColor: "white"
    }

    Text {
        id: radio
        text: "Radio Name"
        elide: Text.ElideRight
        color: listEntry.textColor
        font.pointSize: 15
        minimumPointSize: 12
        font.bold: false

        width: listEntry.width - indicatorBox.width - listEntry.margins*3
        anchors.verticalCenter: listEntry.verticalCenter
        anchors.left: indicatorBox.right
        fontSizeMode: Text.HorizontalFit
        anchors.leftMargin: listEntry.margins
    }

    Text {
        id: time
        text: "time:"
        color: listEntry.textColor
        font.pointSize: 10
        opacity: listEntry.timeEnabled ? 1 : 0

        anchors.bottom: parent.bottom
        anchors.bottomMargin: listEntry.margins
        anchors.left: indicatorBox.right
        anchors.leftMargin: 0
    }

    Text {
        id: timeFrame
        text: "(default)"
        color: listEntry.textColor
        font.pointSize: time.font.pointSize
        opacity: listEntry.timeEnabled ? 1 : 0

        anchors.bottom: parent.bottom
        anchors.bottomMargin: listEntry.margins
        anchors.left: time.right
        anchors.leftMargin: listEntry.margins * 2
    }

    Rectangle {
        id: topLine
        opacity: 0
        color: listEntry.separatorColor
        height: listEntry.margins / 4
        width: parent.width
        anchors.bottom: parent.bottom
    }

    states: [
        State {
            name: "selected"

            PropertyChanges {
                target: background
                opacity: 1
            }
        }
    ]
}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.75}
}
##^##*/
