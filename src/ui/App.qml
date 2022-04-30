
import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    width: Constants.width ? Constants.width : 800
    height: Constants.height ? Constants.height : 450

    visible: true
    title: "IPi-Radio"

    MainWindow {
        id: mainWindow
    }

    onWidthChanged: mainWindow.width = width;
    onHeightChanged: mainWindow.height = height;
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/
