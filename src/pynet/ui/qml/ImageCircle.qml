import QtQuick 2.15
import QtQuick.Controls 2.15

    Rectangle {
        property string imgSource: ""

        color: "#776985"
        radius: 80
        width: 80
        height: 80
        opacity: 1
        border {
            color: "white"
            width: 2
        }

        anchors {
            top:  parent.top
            left: parent.left
        }

        Image {
            id: img
            source: imgSource
            fillMode: Image.PreserveAspectCrop
            width: 48
            height: 48
            anchors.centerIn: parent
        }


    }