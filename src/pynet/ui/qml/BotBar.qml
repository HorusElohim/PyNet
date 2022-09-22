import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

    Rectangle {
            Layout.alignment: Qt.AlignBottom
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"

            Clock {
                Layout.fillWidth: true
                Layout.fillHeight: true
                anchors.left: parent.left
                anchors.bottom: parent.bottom
            }

            LogMessage {
                Layout.fillWidth: true
                Layout.fillHeight: true
                anchors.right: parent.right
                anchors.bottom: parent.bottom
            }
    }
