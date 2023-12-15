
import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    width: 800
    height: 450

    visible: true
    title: "IPi-Radio"

    Connections {
        target: controller

        function onWaitingNetworkState() {
            splashScreen.message = "Waiting for network";
        }
        function onWaitingServerState() {
            splashScreen.message = "Starting webserver";
        }
        function onWaitingDone() {
            console.log("init done");

            mainWindow.visible = true;
            splashScreen.hideBackground();
            splashScreen.opacity = 0;
        }
    }

    MainWindow {
        id: mainWindow
        anchors.fill: parent
        visible: false
    }

    SplashScreen {
        id: splashScreen
        anchors.fill: parent

        version: controller.version_text

        Behavior on opacity {
            NumberAnimation {
                duration: 1000
                //easing.type: Easing.InOutSine
            }
        }
    }
}


/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/
