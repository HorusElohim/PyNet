import QtQuick 2.15
import QtQuick.Controls 2.15


     Button {

        anchors {
            right: parent.right
            top: parent.top
            rightMargin: 5
        }

        id: exiter
        width: 22
        height: 22
        opacity: 0.5


        Image {
            id: cross
            source: "../images/close.png"
            fillMode: Image.Stretch
            anchors.fill: parent
        }

        visible: true
        clip: false
        checked: false
        checkable: false

        background: Rectangle {
            color: exiter.hovered ? 'darkgrey' : 'transparent'
            anchors.fill: parent
            radius: 20
        }

        Connections {
            target: exiter
            function onClicked() {
                Qt.callLater(Qt.quit)
            }
        }
    }