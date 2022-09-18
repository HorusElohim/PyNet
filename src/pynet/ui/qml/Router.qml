import QtQuick 2.15
import QtQuick.Controls 2.15

    Rectangle {
        color: "#250542"
        height: 80
        radius: 50
        anchors {
            top:  topBar.bottom
            topMargin: 5
            right: parent.right
            rightMargin: 1
            left: parent.left
            leftMargin: 1
        }

        Image {
            id: routerImg
            source: "./images/router.png"
            fillMode: Image.PreserveAspectCrop
            width: 32
            height: 32
            anchors {
                top: parent.top
                topMargin: 18
                left: parent.left
                leftMargin: 15
            }
        }

        PNText {
            id: modelText
            anchors {
                top: parent.top
                topMargin: 8
                left: routerImg.right
                leftMargin: 10
            }
            text: appVm.upnp.router.model
        }

        PNText {
            id: modelDesc
            anchors {
                top: parent.top
                topMargin: 40
                left: routerImg.right
                leftMargin: 10
            }
            text: appVm.upnp.router.status
        }

        PNText {
            id: ipText
            anchors {
                top: parent.top
                topMargin: 8
                right: parent.right
                rightMargin: 20
            }
            text: appVm.upnp.router.ip
        }

        PNText {
            id: natText
            anchors {
                top: parent.top
                topMargin: 40
                right: parent.right
                rightMargin: 20
            }
            text: appVm.upnp.router.nat
        }

    }