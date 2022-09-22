import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ApplicationWindow  {
    title: "PyNet"
    width: 500
    height: 360
    minimumWidth: 500
    minimumHeight: 200
    visible: true

    opacity: 0.85
    color: "transparent"

//        flags: Qt.CustomizeWindowHint |  Qt.Window
    flags: Qt.FramelessWindowHint |  Qt.Window

    Background {
        id: backgroundComponent
    }

    MouvableWindow {}
}