import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ApplicationWindow  {
    id: appWindow
    title: "PyNet"
    width: 500
    height: 400
    minimumWidth: 350
    minimumHeight: 350
    visible: true

    opacity: 0.85
    color: "transparent"

    flags: Qt.CustomizeWindowHint |  Qt.Window

    property string logMessage: ""

    Background {
        id: backgroundComponent
    }

    TopBar {
        id: topBar
    }

    MouvableWindow {}

    RouterCard {
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

    ExitButton {}



}
