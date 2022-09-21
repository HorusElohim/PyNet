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
           Layout.alignment: Qt.AlignTop | Qt.AlignLeft
        }

        RouterCard {
            id : routerCard
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
        }

        DNSCard {
            id : routerCard2
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
        }

        BotBar {
            Layout.fillWidth: true
             Layout.fillHeight: true
            Layout.alignment: Qt.AlignBottom | Qt.AlignCenter
            id: botBar
        }

    }
}
