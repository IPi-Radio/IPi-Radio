
import QtQuick 2.12
import QtQuick.Window 2.12


Rectangle {
    anchors.margins: 10
    color: "black"
    radius: 10

    property string message
    property string version

    Rectangle {
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter

        width: title.width * 1.2
        height: title.height

        radius: 10
        color: "white"

        Text {
            id: title
            anchors.centerIn: parent
            text: "IPi-Radio " + version

            color: "black"
            font.pixelSize: 12
        }
    }

    Rectangle {
        anchors.centerIn: parent
        width: splashMessage.width * 1.1
        height: splashMessage.height

        radius: 10
        color: "#e56565"

        Text {
            id: splashMessage
            anchors.centerIn: parent
            text: message

            color: "white"
            font.bold: true
            font.pixelSize: 40
        }
    }

    function hideBackground() {
        color = "#000000ff"
    }
}
