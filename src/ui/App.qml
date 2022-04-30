
import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    width: 800
    height: 450

    visible: true
    title: "IPi-Radio"

    MainWindow {
        id: mainWindow
        anchors.fill: parent
    }

    onWidthChanged: mainWindow.width = width;
    onHeightChanged: mainWindow.height = height;
}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/
