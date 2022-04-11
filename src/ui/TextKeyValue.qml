import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    id: textKeyValue
    width: 100
    height: key.paintedHeight
    color: "#00ffffff"

    property color textColor: "black"
    property int textSize: 10
    property int spacing: 5

    property alias keyText: key.text
    property alias valueText: value.text


    Text {
        id: key
        width: parent.width / 2 - textKeyValue.spacing
        text: "key"
        color: textKeyValue.textColor
        horizontalAlignment: Text.AlignRight
        font.pointSize: textKeyValue.textSize

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
    }

    Text {
        id: value
        width: parent.width / 2 - textKeyValue.spacing
        text: "value"
        color: textKeyValue.textColor
        horizontalAlignment: Text.AlignLeft
        font.pointSize: textKeyValue.textSize

        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:2}
}
##^##*/
