import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

     Button {
        Layout.preferredWidth: 22
        Layout.preferredHeight: 22
        id: exiter
        opacity: 0.5

        Image {
            id: cross
            source: "./images/close.png"
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