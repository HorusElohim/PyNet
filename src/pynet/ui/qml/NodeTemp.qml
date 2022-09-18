import QtQuick 2.15
import QtQuick.Controls 2.15
import MyNode 1.0

    Node {
        id: self
        visible: true
        width: 110
        height: 110
        x: 20
        y: 45

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

                    Text {
            		    text: self.name
        	        }
                }
        }

        MouseArea {
            anchors.fill: parent
            drag.target: self
            drag.axis: Drag.XAndYAxis
            drag.minimumX: 20
            drag.maximumX: parent.width - 100 - 20
            drag.minimumY: 45
            drag.maximumY: parent.height - 100 - 45
        }

    }