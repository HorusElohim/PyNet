from PySide6.QtCore import QTimer, QObject, Signal
from . import LOG


class LogMessage(QObject):
    updated = Signal(str, arguments=['logMessage'])

    def __init__(self):
        super(LogMessage, self).__init__()
        LOG.log.debug('LogMessage constructed')

    def update_message(self, message: str):
        self.updated.emit(message)
        LOG.log.debug(f"log message: {message}")
