import QtQuick 2.15
import QtQuick.Controls 2.15

    Rectangle {
        color: "#250542"
        height: 80
        radius: 80
        border {
            color: "black"
        }


    ImageCircle {
            id: routerImageCircle
            imgSource: "./images/router.png"
        }

        PNText {
                id: routerModelText
                text: appVm.upnp.router.model
                font.pointSize: 11
            anchors {
                top:  parent.top
                topMargin: 10
                left: routerImageCircle.right
                leftMargin: 22
            }
        }

        PNText {
                id: routerStatusText
                text: appVm.upnp.router.status
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
                text: appVm.upnp.router.ip
                font.pointSize: 11
            anchors {
                bottom:  parent.bottom
                bottomMargin: 16
                left: routerImageCircle.right
                leftMargin: 22
            }
        }

        PNText {
                id: routerNatText
                text: appVm.upnp.router.nat
                font.pointSize: 11
            anchors {
                bottom:  parent.bottom
                bottomMargin: 16
                right: parent.right
                rightMargin: 22
            }
        }
    }