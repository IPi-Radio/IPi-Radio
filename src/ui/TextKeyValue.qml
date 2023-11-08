import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    id: textKeyValue
    width: 100
    height: value.paintedHeight * 1.05
    color: "#00ffffff"

    property color textColor: "black"
    property int textSize: 10
    property int spacing: 5

    property alias keyText: key.text
    property alias valueText: value.text

    Rectangle {
        id: keyBack
        height: key.paintedHeight
        width: key.paintedWidth + 10
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.verticalCenter: parent.verticalCenter

        color: "white"
        radius: 10

        Text {
            id: key
            anchors.centerIn: parent
            color: "black"
            text: "key"
            font.pointSize: textKeyValue.textSize - 2

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Text {
        id: value
        text: "value"
        color: textKeyValue.textColor
        font.pointSize: textKeyValue.textSize
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        anchors.fill: parent
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:2}
}
##^##*/
