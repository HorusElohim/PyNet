import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

    Rectangle {
        id: topRectBanner
        radius: 200
        color: "white"
        height: 30
        opacity: 1
        Layout.minimumWidth: 170
        Layout.minimumHeight: 25

        RowLayout {
            anchors.fill: parent
            anchors.margins: 5
            Layout.alignment: Qt.AlignCenter

            RowLayout {
                Text {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    font.family: "Cascadia Code Extralight"
                    text: appVm.info.name + " " + appVm.info.version
                    font.pointSize: 13
                    color: "#3C096C"
                    opacity: 1
                }
                ExitButton {
                }
            }
        }


    }
