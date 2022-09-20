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
            }

            LogMessage {
                Layout.fillWidth: true
                Layout.fillHeight: true
                anchors.right: parent.right
            }
    }
