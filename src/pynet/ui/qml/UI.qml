import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ApplicationWindow  {
    id: appWindow
    title: "PyNet"
    width: 400
    height: 400
    minimumWidth: 250
    minimumHeight: 250
    visible: true

    opacity: 0.85
    color: "transparent"

    flags: Qt.CustomizeWindowHint |  Qt.Window

    property string logMessage: ""

    Background {
        id: backgroundComponent
    }

    TopBar {}

    DropArea {}

    MouvableWindow {}

    Clock {}

    LogMessage {}

    ExitButton {}

}
