import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ApplicationWindow  {
    id: appWindow
    title: "PyNet"
    width: 500
    height: 280
    minimumWidth: 350
    minimumHeight: 350
    visible: true

    opacity: 0.85
    color: "transparent"

//    flags: Qt.CustomizeWindowHint |  Qt.Window
    flags: Qt.FramelessWindowHint |  Qt.Window

    property string logMessage: ""

    Background {
        id: backgroundComponent
    }




    MouvableWindow {}
        TopBar {
           id: topBar
           ratio: 0.4
           ExitButton {}
    }


    RouterCard {
        id : routerCard
        anchors {
            top:  topBar.bottom
            topMargin: 10
            right: parent.right
            rightMargin: 10
            left: parent.left
            leftMargin: 10
        }

    }

//    DropArea {}

    PNCanvas {
        id: appCanvas
        Node {}
    }

    Clock {}

    LogMessage {}





}
