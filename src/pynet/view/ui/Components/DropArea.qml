import QtQuick 2.15
import QtQuick.Controls 2.15


    DropArea {
        id: dropArea;
        anchors.fill: parent

        onEntered: (drag) => {
            drag.accept (Qt.LinkAction);
            backgroundComponent.opacity = 0.5
        }
        onDropped: (drop) => {
            console.log(drop.urls)
            dropController.output_path(drop.urls)
            backgroundComponent.opacity = 1
        }
        onExited: {
            backgroundComponent.opacity = 1
        }
    }