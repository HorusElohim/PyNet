import QtQuick 2.15
import QtQuick.Controls 2.15

    Text {
        anchors {
            bottom: parent.bottom
            bottomMargin: 12
            right: parent.right
            rightMargin: 12
        }
        font.family: "Cascadia Code Extralight"
        text: appVm.clock.time  // used to be; text: "16:38:33"
        font.pointSize: 11
        color: "white"
        opacity: 1
    }
