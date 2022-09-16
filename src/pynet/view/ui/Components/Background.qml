import QtQuick 2.15
import QtQuick.Controls 2.15


    Rectangle {
        id: backgroundRect
        anchors.fill: parent


        Image {
            sourceSize.width: backgroundRect.width
            sourceSize.height: backgroundRect.height
            source:  "../images/background2.png"
            fillMode: Image.PreserveAspectCrop

        }
    }