import QtQuick 2.15
import QtQuick.Controls 2.15

    Rectangle {
        color: "transparent"
        height: 80
        radius: 80

        Rectangle {
            color: "#250542"
            width: parent.width
            height: parent.height
            radius: 80
            visible: appVm.router_card.visible_body
            border {
                color: "black"
            }

            PNText {
                id: routerModelText
                text: appVm.router_card.info.model
                font.pointSize: 11
            anchors {
                top:  parent.top
                topMargin: 10
                left: parent.left
                leftMargin: 102
                }
            }

            PNText {
                    id: routerStatusText
                    text: appVm.router_card.info.sip
                    font.pointSize: 11
                anchors {
                    top:  parent.top
                    topMargin: 10
                    right: parent.right
                    rightMargin: 22
                }
            }

            PNText {
                    id: routerIpText
                    text: appVm.router_card.info.ip
                    font.pointSize: 11
                anchors {
                    bottom:  parent.bottom
                    bottomMargin: 16
                    left: parent.left
                    leftMargin: 102
                }
            }

            PNText {
                    id: routerNatText
                    text: appVm.router_card.info.nat
                    font.pointSize: 11
                anchors {
                    bottom:  parent.bottom
                    bottomMargin: 16
                    right: parent.right
                    rightMargin: 22
                }
            }

        }
        ImageCircle {
                id: routerImageCircle
                imgSource: "./images/router2.png"
                border.color: appVm.router_card.color
                MouseArea {
                    id: area
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                       appVm.router_card.visible_body = !appVm.router_card.visible_body
                    }
                }
        }
    }