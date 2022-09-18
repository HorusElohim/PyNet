import QtQuick 2.15
import QtQuick.Controls 2.15

    PNText {
        anchors {
            bottom: parent.bottom
            bottomMargin: 12
            left: parent.left
            leftMargin: 12
        }

        text: appVm.log.message  // used to be; text: "16:38:33"
    }
