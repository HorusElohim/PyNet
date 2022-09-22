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
                Layout.alignment: Qt.AlignTop | Qt.AlignLeft
        }

        VerticalLine {}

        RouterCard {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
        }

        VerticalLine {}

        PynetCard {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
        }

        BotBar {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignBottom | Qt.AlignCenter
        }

    }
}
