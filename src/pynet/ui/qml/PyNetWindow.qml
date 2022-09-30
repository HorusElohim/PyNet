import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ApplicationWindow  {
    title: "PyNet"
    width: 480
    height: 400
    minimumWidth: 500
    minimumHeight: 200
    visible: true

    opacity: 0.95
    color: "transparent"

//        flags: Qt.CustomizeWindowHint |  Qt.Window
    flags: Qt.FramelessWindowHint |  Qt.Window

    Background {
        id: backgroundComponent
    }

    MouvableWindow {}


}