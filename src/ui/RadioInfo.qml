import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    id: radioInfo
    width: 800
    height: 600
    //height: column.height + border.width * 4

    color: "black"
    border.color: "white"
    border.width: 8
    radius: 20

    property color textColor: "white"
    property alias versionText: versionNumberText.text
    property alias statusText: playStatus.valueText
    property alias radioName: radioName.text
    property alias dlsText: dlsText.text
    property alias clock: clock.text
    property alias codecText: codec.valueText
    property alias countryText: country.valueText
    property alias webAddress: webUrl.valueText

    Rectangle {
        id: versionNumberRect
        width: versionNumberText.paintedWidth + 10
        //height: 20
        height: parent.border.width * 3

        color: parent.color
        radius: 5

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.leftMargin: parent.height * 0.06

        Text {
            id: versionNumberText
            anchors.fill: parent
            text: "v0.0"
            color: radioInfo.textColor
            font.pixelSize: parent.height * 0.9
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Column {
        id: columnTop
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: columnBottom.top
        anchors.bottomMargin: radioInfo.border.width
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: radioInfo.border.width * 2

        property int textSpace: height - playStatus.height - radioInfo.border.width

        TextKeyValue {
            id: playStatus
            width: parent.width
            textColor: radioInfo.textColor
            textSize: 10
            keyText: "Status:"
            valueText: "unknown"
        }
        Text {
            id: radioName
            width: radioInfo.width - radioInfo.border.width*4
            text: "IPi-Radio"
            elide: Text.ElideRight
            color: radioInfo.textColor
            font.pointSize: 45
            font.bold: (height < 25) ? true : false
            minimumPointSize: 20

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            fontSizeMode: Text.Fit
            anchors.horizontalCenter: parent.horizontalCenter

            height: parent.textSpace * 0.5
        }
        Text {
            id: dlsText
            width: radioInfo.width - radioInfo.border.width*4
            text: "radio text (DLS)"
            elide: Text.ElideMiddle
            color: radioInfo.textColor
            font.pointSize: 15
            minimumPointSize: 10

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignTop
            fontSizeMode: Text.Fit
            //wrapMode: Text.WordWrap
            //maximumLineCount: 1

            anchors.horizontalCenter: parent.horizontalCenter

            height: parent.textSpace * 0.1
        }
        Text {
            id: clock
            width: parent.width
            text: "00:00:00"
            color: radioInfo.textColor
            font.pointSize: 35
            minimumPointSize: 20

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignBottom
            fontSizeMode: Text.Fit

            height: parent.textSpace * 0.4
        }
    }

    Column {
        id: columnBottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottomMargin: radioInfo.border.width * 2

        ToolSeparator {
            width: parent.width - radioInfo.border.width * 2
            height: radioInfo.border.width
            hoverEnabled: false
            enabled: false
            anchors.horizontalCenter: parent.horizontalCenter
        }
        TextKeyValue {
            id: codec
            width: parent.width
            textColor: radioInfo.textColor
            textSize: 10
            keyText: "codec:"
            valueText: "---"
        }
        TextKeyValue {
            id: country
            width: parent.width
            textColor: radioInfo.textColor
            textSize: 10
            keyText: "country:"
            valueText: "---"
        }
        ToolSeparator {
            width: parent.width - radioInfo.border.width * 2
            height: radioInfo.border.width
            hoverEnabled: false
            enabled: false
            anchors.horizontalCenter: parent.horizontalCenter
        }
        TextKeyValue {
            id: webUrl
            width: parent.width
            textColor: radioInfo.textColor
            textSize: 10
            keyText: "webUI address:"
            valueText: "---"
        }
    }

    state: "base"
    states: [
        State {
            name: "base"
            PropertyChanges {
                target: radioInfo
                border.color: "white"
            }
        },
        State {
            name: "auto"
            PropertyChanges {
                target: radioInfo
                border.color: "green"
            }
        }
    ]

    Behavior on border.color {
        ColorAnimation {
            duration: 500
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.9}
}
##^##*/
