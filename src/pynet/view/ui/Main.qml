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

    flags: Qt.CustomizeWindowHint |  Qt.Window

    property QtObject clockController
    property QtObject dropController

    property string clockTime: "00:00:00"
    property string appName: ""
    property string appVersion: ""

    Background {
        id: backgroundComponent
    }

    Rectangle {
        id: topRectBanner
        color: "white"

        anchors.top: parent.top
        anchors.left: parent.left
        height: 24
        width: parent.width
        opacity: 1

        Text {
            anchors {
                bottom: parent.bottom
                bottomMargin: 2
                left: parent.left
                leftMargin: 5
            }
            font.family: "Cascadia Code Extralight"
            text: appName + " " + appVersion
            font.pointSize: 13
            color: "#3C096C"
            opacity: 1
        }
    }

    DropArea {}

    MouvableWindow {}

    Clock {}

    ExitButton {}
}