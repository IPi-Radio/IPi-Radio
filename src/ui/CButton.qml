import QtQuick 2.12
import QtQuick.Controls 2.12

Button {
    id: cbutton

    //width: Math.max(buttonBackground ? buttonBackground.implicitWidth : 0,
    //                   textItem.implicitWidth + leftPadding + rightPadding)
    //height: Math.max(buttonBackground ? buttonBackground.implicitHeight : 0,
    //                    textItem.implicitHeight + topPadding + bottomPadding)

    //width: keyIndicator.width + textItem.paintedWidth + leftPadding + rightPadding
    //height: textItem.paintedHeight + topPadding + bottomPadding
    width: 250
    height: 70

    leftPadding: 4
    rightPadding: 4

    text: "My Button"

    property bool indicatorEnabled: true
    property int indicatorSize: 20
    property string indicatorString: "0"

    property alias indicatorColor: keyIndicator.color
    property alias indicatorTextColor: keyIndicatorKey.color
    property alias textColor: textItem.color
    property alias textSize: textItem.font.pointSize
    property alias border: buttonBackground.border
    property alias radius: buttonBackground.radius

    background: buttonBackground
    Rectangle {
        id: buttonBackground
        radius: 2
        //color: "#313431"
        color: "#313431"
        border.width: 1
        gradient: Gradient {
            orientation: Gradient.Vertical
            GradientStop {
                id: pos1
                position: 0
                color: "#2f2f2f"
            }

            GradientStop {
                id: pos2
                position: 0.5
                color: "#000000"
            }

            GradientStop {
                id: pos3
                position: 1
                color: "#131313"
            }
        }
        border.color: "black"

        Behavior on border.color {
            ColorAnimation {
                duration: 200
            }
        }
    }

    contentItem: contentItem
    Rectangle {
        id: contentItem
        anchors.fill: parent
        color: "#00ffffff"

        Rectangle {
            id: keyIndicator
            radius: 100
            width: cbutton.indicatorSize
            height: width
            opacity: cbutton.indicatorEnabled ? 1 : 0
            color: "#008aff"

            x: cbutton.width/2 - textItem.paintedWidth/2 - width*2
            anchors.verticalCenter: parent.verticalCenter

            Text {
                id: keyIndicatorKey
                anchors.fill: parent
                color: "white"
                opacity: cbutton.indicatorEnabled ? 1 : 0
                text: "0"
                font.pointSize: textItem.font.pointSize - 1

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
        Text {
            id: textItem
            text: cbutton.text
            color: "white"
            font.pointSize: 10

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.fill: parent
            //anchors.leftMargin: keyIndicator.width
            anchors.leftMargin: 0
        }
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onPressed: cbutton.state = "pressed"
        onReleased: {
            if (containsMouse)
                cbutton.state = "selected"
            else
                cbutton.state = "base"
        }

        onContainsMouseChanged: {
            if (containsMouse)
                cbutton.state = "selected"
            else
                cbutton.state = "base"
        }
        onClicked: cbutton.clicked()
    }

    states: [
        State {
            name: "selected"
            PropertyChanges {
                target: buttonBackground
                border.color: "#585858"
            }
        },
        State {
            name: "pressed"
            PropertyChanges {
                target: buttonBackground
                border.color: "white"
            }
            PropertyChanges {
                target: pos1
                position: 0.5
            }
            PropertyChanges {
                target: pos2
                position: 1
            }
            PropertyChanges {
                target: pos3
                position: 0
            }
        }
    ]
}
/*##^##
Designer {
    D{i:0;height:60;width:200}
}
##^##*/
