import QtQuick 2.12
import QtQuick.Controls 2.12

Button {
    id: cbutton

    width: 250
    height: 70

    leftPadding: 4
    rightPadding: 4

    text: "My Button"

    property bool indicatorEnabled: true
    property int indicatorSize: 20
    property string indicatorString: "0"
    property bool altMode: false

    property alias indicatorColor: keyIndicator.color
    property alias indicatorTextColor: keyIndicator.textColor
    property alias textColor: textItem.color
    property alias textSize: textItem.font.pointSize
    property alias border: buttonBackground.border
    property alias radius: buttonBackground.radius

    background: buttonBackground
    Rectangle {
        id: buttonBackground
        radius: 2
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

        KeyIndicator {
            id: keyIndicator

            width: indicatorSize
            height: width

            anchors {
                left: parent.left
                leftMargin: buttonBackground.border.width * 2
                verticalCenter: parent.verticalCenter
            }

            opacity: indicatorEnabled ? 1 : 0
            color: parent.color

            text: indicatorString
            textColor: "white"
            textFont.pointSize: textItem.font.pointSize - 1
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

    state: "base"
    states: [
        State {
            name: "base"
            PropertyChanges {
                target: buttonBackground
                border.color: cbutton.altMode ? "#008000" : "black"
            }
        },
        State {
            name: "selected"
            PropertyChanges {
                target: buttonBackground
                border.color: cbutton.altMode ? "#00c500" : "#585858"
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

    function setSelected(selection) {
        if (selection === true)
            state = "selected";
        else
            state = "base";
    }

}
/*##^##
Designer {
    D{i:0;height:60;width:200}
}
##^##*/
