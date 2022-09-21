import QtQuick 2.15
import QtQuick.Controls 2.15

    Rectangle {
        property string imgSource: ""

        color: "black"
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
            width: 70
            height: 70
            anchors.centerIn: parent
        }


    }