import pkg_resources
from PySide6.QtCore import QUrl


def url(qml_file: [str]):
    return QUrl.fromLocalFile(pkg_resources.resource_filename('pynet', qml_file))


from PySide6.QtCore import QtInfoMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg
from PySide6 import QtCore
from .. import LOG

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
    LOG.log.debug(msg)


QtCore.qInstallMessageHandler(qt_message_handler)
LOG.log.debug("qInstallMessageHandler activated")