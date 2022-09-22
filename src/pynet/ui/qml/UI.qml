import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

PyNetWindow {
    id: appWindow

    ColumnLayout {
        anchors.fill: parent
        Layout.fillHeight: true
        anchors.margins: 1
        anchors.leftMargin: 40
        spacing: 1

        TopBar {
                id: topBar
                Layout.alignment: Qt.AlignTop | Qt.AlignLeft
        }


        VerticalLine {}

        RouterCard {
            id : routerCard
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
        }

        VerticalLine {}

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
