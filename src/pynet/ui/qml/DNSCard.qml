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
            visible: appVm.dns_card.visible_body
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
                    Layout.fillWidth: true
                    PNText {
                            id: dnsModelText
                            text: "Port: " + appVm.dns_card.info.mapped_port
                            font.pointSize: 11
                            }
                    PNText {
                        id: dnsNatText
                        text: "Users: " + appVm.dns_card.info.n_clients
                        font.pointSize: 11
                    }
                }
                ColumnLayout{
                    Layout.alignment: Qt.AlignCenter | Qt.AlignRight
                    Layout.fillHeight: true

                    PNText {
                        id: dnsStatusText
                        text: "DNS: " + appVm.dns_card.info.dns_server
                        font.pointSize: 11
                    }



                }
            }
        }

        ImageCircle {
                id: dnsImageCircle
                imgSource: "./images/pynet-5.png"
                border.color: appVm.dns_card.color
                MouseArea {
                    id: area
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                       appVm.dns_card.visible_body = !appVm.dns_card.visible_body
                    }
                }
        }
    }