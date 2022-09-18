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

    Router {
        id: routerBar
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
