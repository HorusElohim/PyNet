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
    minimumWidth: 250
    minimumHeight: 250

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

    Rectangle {
        id: avatarRectBorder
        width: 110
        height: 110
        radius: 110
        color: "#4fd66f"
        x: 20
        y: 45

              border {
                color: black
                width: 1
            }

        Rectangle {
            id: avatarRect
            width: 100
            height: 100
            radius: 100
            color: white
            x: 5
            y: 5
            border {
                color: black
                width: 1
            }

            MouseArea {
                anchors.fill: parent
                drag.target: avatarRectBorder
                drag.axis: Drag.XAndYAxis
                drag.minimumX: 20
                drag.maximumX: appWindow.width - 100 - 20
                drag.minimumY: 45
                drag.maximumY: appWindow.height - 100 - 45
            }
        }
    }



    Clock {}

    LogMessage {}

    ExitButton {}

}
