import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

PyNetWindow {
    id: appWindow

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 1
        spacing: 10

        TopBar {
           id: topBar
           Layout.alignment: Qt.AlignTop | Qt.AlignCenter
        }

        RouterCard {
            id : routerCard
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
        }

        BotBar {
            id: botBar
        }

    }
}
