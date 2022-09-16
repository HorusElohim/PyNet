import QtQuick 2.15
import QtQuick.Controls 2.15

import "Components"


ApplicationWindow {
    id: appWindow
    visible: true
    title: "PyNet"
    width: 400
    height: 400
    opacity: 0.85
    color: "transparent"
    minimumWidth: 200
    minimumHeight: 150

    flags: Qt.CustomizeWindowHint |  Qt.Window

    property QtObject logController
    property QtObject clockController
    property QtObject dropController

    property string clockTime: "00:00:00"
    property string appName: ""
    property string appVersion: ""
    property string logMessage: ""

    Background {
        id: backgroundComponent
    }

    TopBar {}

    DropArea {}

    MouvableWindow {}

    Clock {}

    LogMessage {}

    ExitButton {}

}
