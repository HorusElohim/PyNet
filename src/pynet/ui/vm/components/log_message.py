from PySide6.QtCore import QObject, Signal, Property, Slot
from . import LOG


class LogMessage(QObject):
    message_changed = Signal(str)

    def __init__(self):
        super(LogMessage, self).__init__()
        self._message = "Ready"
        LOG.log.debug('LogMessage constructed')

    @Property(str, notify=message_changed)
    def message(self):
        return self._message

    @Slot(str)
    def update_message(self, msg):
        self._message = msg
        self.message_changed.emit(self._message)
        LOG.log.debug(f"logging: {msg}")
