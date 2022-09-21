import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

    Rectangle {
        color: "transparent"
        height: 80
        radius: 80

        Rectangle {
            color: "black"
            width: parent.width
            height: parent.height
            radius: 80
            visible: appVm.router_card.visible_body
            border {
                color: "black"
            }

            RowLayout{
                anchors.left : parent.left
                anchors.leftMargin: 90
                anchors.top: parent.top
                anchors.topMargin: 5
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 5
                spacing: 10

                ColumnLayout{
                    Layout.alignment: Qt.AlignCenter | Qt.AlignLeft
                    PNText {
                            id: routerModelText
                            text: "Router: " + appVm.router_card.info.model
                            font.pointSize: 11
                            }
                    PNText {
                            id: routerIpPubText
                            text: "Public: " + appVm.router_card.info.public_ip
                            font.pointSize: 11
                    }
                    PNText {
                            id: routerIpLocalText
                            text: "Local: " + appVm.router_card.info.local_ip
                            font.pointSize: 11
                    }
                }
                ColumnLayout{
                    Layout.alignment: Qt.AlignCenter | Qt.AlignLeft
                    Layout.fillHeight: true

                    PNText {
                        id: routerStatusText
                        text: appVm.router_card.info.sip
                        font.pointSize: 11
                    }

                    PNText {
                        id: routerNatText
                        text: appVm.router_card.info.nat
                        font.pointSize: 11
                    }

                    PNText {
                        id: routerUpnpText
                        text: appVm.router_card.info.upnp
                        font.pointSize: 11
                    }

                }
            }
        }

        ImageCircle {
                id: routerImageCircle
                imgSource: "./images/pynet-7.png"
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