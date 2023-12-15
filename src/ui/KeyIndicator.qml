import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    id: keyIndicator

    property alias text: keyIndicatorKey.text
    property alias textColor: keyIndicatorKey.color
    property alias textFont: keyIndicatorKey.font

    radius: 100
    border.width: 3
    border.color: "#008aff"

    Text {
        id: keyIndicatorKey

        anchors.fill: parent

        text: "0"
        color: "black"
        opacity: parent.opacity

        font.pixelSize: (parent.height - parent.border.width*2) * 0.9

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
