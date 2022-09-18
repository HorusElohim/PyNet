import QtQuick 2.15
import QtQuick.Controls 2.15


    Rectangle {
        id: topRectBanner
        radius: 200
        color: "white"

        property double ratio: 1

        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        height: 24
        width: Math.floor(parent.width * ratio)
        opacity: 1

        Text {
            anchors.centerIn : parent
            font.family: "Cascadia Code Extralight"
            text: appVm.info.name + " " + appVm.info.version
            font.pointSize: 13
            color: "#3C096C"
            opacity: 1
        }
    }
