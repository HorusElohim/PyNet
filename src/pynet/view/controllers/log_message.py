from PySide6.QtCore import QTimer, QObject, Signal
from . import CTRL_LOGGER


class LogMessage(QObject):
    updated = Signal(str, arguments=['logMessage'])

    def __init__(self):
        super(LogMessage, self).__init__()
        CTRL_LOGGER.log.debug('LogMessage constructed')

    def update_message(self, message: str):
        self.updated.emit(message)
        CTRL_LOGGER.log.debug(f"log message: {message}")
