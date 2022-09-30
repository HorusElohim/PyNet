import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

PyNetWindow {
    id: appWindow

    Rectangle {
        id: appRectWindow
        anchors.fill: parent
        radius: 30
        color: 'transparent'
        opacity: 0.85

        ColumnLayout {
            anchors.fill: parent
            Layout.fillHeight: true
            anchors.margins: 10
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

        DropArea {
            id: dropArea;
            anchors.fill: parent
            onEntered: (drag) => {
                appRectWindow.color = "#50a125";
                drag.accept (Qt.LinkAction);
            }
            onDropped: (drop) => {
                console.log(drop.urls)
                appRectWindow.color = "transparent"
            }
            onExited: {
                appRectWindow.color = "transparent";
            }
        }

    }
}
