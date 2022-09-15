import QtQuick 2.15
import QtQuick.Controls 2.15


     Button {
        anchors.right: parent.right
        anchors.top: parent.top
        id: exiter
        width: 32
        height: 32
        opacity: 0.5

        Image {
            id: cross
            source: "../images/close-512.png"
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
        }

        Connections {
            target: exiter
            function onClicked() {
                Qt.callLater(Qt.quit)
            }
        }
    }