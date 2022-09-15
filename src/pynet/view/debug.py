from PySide6.QtCore import QtInfoMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg
from PySide6 import QtCore
from . import UI_LOGGER

QML_MSG_STATUS = {
    QtInfoMsg: 'INFO',
    QtWarningMsg: 'WARNING',
    QtCriticalMsg: 'CRITICAL',
    QtFatalMsg: 'FATAL'
}


def qt_message_handler(mode, context, message):
    status = "DEBUG"

    if mode in QML_MSG_STATUS:
        status = QML_MSG_STATUS[mode]

    msg = f'{status}: {message}, {context.file}, {context.line}'
    UI_LOGGER.log.debug(msg)


QtCore.qInstallMessageHandler(qt_message_handler)
UI_LOGGER.log.debug("qInstallMessageHandler activated")
