import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Shapes 1.15

Rectangle {
    id: radioInfo
    width: 600
    height: 400

    color: "black"
    radius: 20

    property color textColor: "white"
    property alias versionText: versionNumberText.text
    property alias statusText: statusText.status
    property alias radioName: radioName.text
    property alias dlsText: dlsText.text
    property alias clock: clock.text
    property alias codecText: codec.valueText
    property alias countryText: country.valueText
    property alias webAddress: webUrl.valueText

    Rectangle {
        id: versionNumberRect
        width: versionNumberText.paintedWidth + 10
        height: versionNumberText.paintedHeight

        color: parent.color
        radius: 5

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.leftMargin: parent.radius

        Text {
            id: versionNumberText
            anchors.fill: parent
            text: "v0.0"
            color: radioInfo.textColor
            font.pointSize: 10
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Column {
        id: columnTop
        anchors.left: parent.left
        anchors.leftMargin: 0

        anchors.right: parent.right
        anchors.rightMargin: 0

        anchors.top: parent.top
        //anchors.topMargin: radioInfo.border.width * 2
        anchors.topMargin: 0

        anchors.bottom: columnBottom.top
        anchors.bottomMargin: radioInfo.border.width

        property int textSpace: height - statusText.height - radioInfo.border.width

        Shape {
            id: versionShape
            width: statusText.paintedWidth + padding
            height: statusText.paintedHeight
            anchors.horizontalCenter: parent.horizontalCenter

            property int padding: 20

            ShapePath {
                id: p
                fillColor: "white"
                strokeWidth: 0
                startX: 0
                startY: 0

                property alias w: versionShape.width
                property alias h: versionShape.height

                PathLine { x: versionShape.padding / 2; y: p.h }
                PathLine { x: p.w - versionShape.padding / 2; y: p.h }
                PathLine { x: p.w; y: 0 }
                PathLine { x: 0; y: 0 }

                Behavior on fillColor {
                    ColorAnimation {
                        duration: animSpeed
                    }
                }
                Behavior on strokeColor {
                    ColorAnimation {
                        duration: animSpeed
                    }
                }
            }

            Text {
                id: statusText
                width: radioInfo.width * 0.76
                anchors.centerIn: parent
                font.pointSize: 10
                color: "black"

                property string status: "unknown"
                text: "Status: " + status

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.WordWrap

                Behavior on color {
                    ColorAnimation {
                        duration: animSpeed
                    }
                }
            }
        }

        Text {
            id: radioName
            width: radioInfo.width - radioInfo.border.width * 4
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
            PropertyChanges {
                target: p
                fillColor: "white"
                strokeColor: "white"
            }
            PropertyChanges {
                target: statusText
                color: "black"
            }
        },
        State {
            name: "auto"
            PropertyChanges {
                target: radioInfo
                border.color: "green"
            }
            PropertyChanges {
                target: p
                fillColor: "green"
                strokeColor: "green"
            }
            PropertyChanges {
                target: statusText
                color: "white"
            }
        }
    ]

    property int animSpeed: 500

    Behavior on border.color {
        ColorAnimation {
            duration: animSpeed
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.9}
}
##^##*/
