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
            visible: appVm.pynet_card.visible_body

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
                        text: "Users: " + appVm.pynet_card.info.n_clients
                        font.pointSize: 11
                    }

                    PNText {
                        text: "Ping: " + appVm.pynet_card.info.delta_ms + " ms"
                        font.pointSize: 11
                    }

                    PNText {
                        text: "Updated: " + appVm.pynet_card.info.last_update
                        font.pointSize: 11
                    }


                }
                ColumnLayout{
                    Layout.alignment: Qt.AlignCenter | Qt.AlignRight
                    Layout.fillHeight: true

                    PNText {
                        text: "Server: " + appVm.pynet_card.info.server_status
                        font.pointSize: 11
                    }

                    PNText {
                        text: "Hearbeat: " + appVm.pynet_card.info.alive_status
                        font.pointSize: 11
                    }
                }
            }
        }

        ImageCircle {
                id: dnsImageCircle
                imgSource: "./images/pynet-5.png"
                border.color: appVm.pynet_card.color
                MouseArea {
                    id: area
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                       appVm.pynet_card.visible_body = !appVm.pynet_card.visible_body
                    }
                }
        }
    }