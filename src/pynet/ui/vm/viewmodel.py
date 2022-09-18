from PySide6.QtCore import QObject, Slot, Signal, Property
from .components import Clock, Info, LogMessage
from .. import LOG


class ViewModel(QObject):
    _log_message_sig = Signal(str)

    def __init__(self, parent=None):
        super(ViewModel, self).__init__(parent)
        self._clock = Clock()
        self._info = Info()
        self._log = LogMessage()
        self._log_message_sig.connect(self._log.update_message)
        LOG.log.debug("VM Constructed")

    @Property(QObject, constant=True)
    def clock(self):
        return self._clock

    @Property(QObject, constant=True)
    def log(self):
        return self._log

    @Property(QObject, constant=True)
    def info(self):
        return self._info

    def log_message(self, msg):
        self._log_message_sig.emit(msg)
