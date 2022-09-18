import QtQuick 2.15
import QtQuick.Controls 2.15

    PNText {
        anchors {
            bottom: parent.bottom
            bottomMargin: 12
            right: parent.right
            rightMargin: 12
        }
        text: appVm.clock.time
    }
