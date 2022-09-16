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

    flags: Qt.CustomizeWindowHint |  Qt.Window

    property QtObject clockController
    property QtObject dropController

    property string clockTime: "00:00:00"

    Background {
        id: backgroundComponent
    }

    DropArea {}

    MouvableWindow {}

    Clock {}


    ExitButton {}
}