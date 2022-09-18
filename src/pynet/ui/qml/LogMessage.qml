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
        text: appVm.log.message  // used to be; text: "16:38:33"
        font.pointSize: 11
        color: "white"
        opacity: 1

//        Connections {
//            target: logController
//
//            function onUpdated(msg) {
//                logMessage = msg;
//            }
//        }
    }
