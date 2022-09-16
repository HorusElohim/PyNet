import QtQuick 2.15
import QtQuick.Controls 2.15

    Text {

        anchors {
            bottom: parent.bottom
            bottomMargin: 12
            left: parent.left
            leftMargin: 12
        }
        font.family: "Cascadia Code Extralight"
        text: clockTime  // used to be; text: "16:38:33"
        font.pointSize: 13
        color: "white"
        opacity: 1

        Connections {
            target: clockController

            function onUpdated(msg) {
                clockTime = msg;
            }
        }
    }
