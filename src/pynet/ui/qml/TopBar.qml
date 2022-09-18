import QtQuick 2.15
import QtQuick.Controls 2.15


    Rectangle {
        id: topRectBanner
        color: "white"

        anchors.top: parent.top
        anchors.left: parent.left
        height: 24
        width: parent.width
        opacity: 1

        Text {
            anchors {
                bottom: parent.bottom
                bottomMargin: 2
                left: parent.left
                leftMargin: 5
            }
            font.family: "Cascadia Code Extralight"
            text: appVm.info.name + " " + appVm.info.version
            font.pointSize: 13
            color: "#3C096C"
            opacity: 1
        }
    }
