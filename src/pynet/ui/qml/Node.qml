import QtQuick 2.15
import QtQuick.Controls 2.15

     Rectangle {
        id: nodeOuterRect
        width: 110
        height: 110
        radius: 110
        color: "#4fd66f"
        x: 20
        y: 45

        border {
            color: "black"
            width: 1
        }

        Rectangle {
            id: nodeRect
            width: 100
            height: 100
            radius: 100
            color: "white"
            x: 5
            y: 5
            border {
                color: "black"
                width: 1
            }
        }

        MouseArea {
            anchors.fill: parent
            drag.target: nodeOuterRect
            drag.axis: Drag.XAndYAxis
            drag.minimumX: 0
            drag.maximumX: appCanvas.width - 110
            drag.minimumY: 0
            drag.maximumY: appCanvas.height - 110
        }

        Component.onCompleted: {
            console.log("Node Created")
            console.log("Node - Parent" + parent)
        }
    }


