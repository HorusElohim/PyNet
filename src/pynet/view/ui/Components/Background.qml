import QtQuick 2.15
import QtQuick.Controls 2.15


    Rectangle {
        id: mainRect
        anchors.fill: parent


        Image {
            sourceSize.width: mainRect.width
            sourceSize.height: mainRect.height
            source:  "../images/Background2.png"
            fillMode: Image.PreserveAspectCrop

        }
    }