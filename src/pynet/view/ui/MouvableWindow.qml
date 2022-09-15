import QtQuick 2.15
import QtQuick.Controls 2.15

    MouseArea {
            anchors.fill: parent
            property real lastMouseX: 0
            property real lastMouseY: 0
            onPressed: {
                lastMouseX = mouseX
                lastMouseY = mouseY
            }
            onMouseXChanged: appWindow.x += (mouseX - lastMouseX) * 0.6
            onMouseYChanged: appWindow.y += (mouseY - lastMouseY) * 0.6
        }
