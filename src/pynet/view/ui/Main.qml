import QtQuick 2.15
import QtQuick.Controls 2.15

import "Components"


ApplicationWindow {
    id: appWindow
    visible: true
    title: "PyNet"
    width: 400
    height: 600
    opacity: 0.85

    flags: Qt.FramelessWindowHint | Qt.Window

    property QtObject clock
    property string clockTime: "00:00:00"

    MouvableWindow {}
    Background {}
    Clock {}


    ExitButton {}
}