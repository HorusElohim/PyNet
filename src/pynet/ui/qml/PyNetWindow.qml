import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ApplicationWindow  {
    title: "PyNet"
    width: 400
    height: 150
    minimumWidth: 400
    minimumHeight: 150
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