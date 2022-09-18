import QtQuick 2.15
import QtQuick.Controls 2.15

    Rectangle {
        color: "#250542"
        height: 50
        radius: 50
        anchors {
            top:  topBar.bottom
            topMargin: 2
            right: parent.right
            rightMargin: 5
            left: parent.left
            leftMargin: 5
        }

        Image {
            id: routerImg
            source: "./images/router.png"
            fillMode: Image.PreserveAspectCrop
            width: 32
            height: 32
            anchors {
                top: parent.top
                topMargin: 8
                left: parent.left
                leftMargin: 10
            }
        }

        PNText {
            anchors {
                top: parent.top
                topMargin: 8
                right: parent.right
                rightMargin: 15
            }
            text: appVm.upnp.router
        }

        PNText {
            anchors {
                top: parent.top
                topMargin: 8
                left: routerImg.right
                leftMargin: 15
            }
            text: appVm.upnp.ip
        }

    }