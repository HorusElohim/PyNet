from PySide6.QtCore import QObject, Slot, Signal, Property, QThreadPool
from .components import Clock, AppInfo, LogMessage, RouterCard, DNSCard
from .. import LOG


class ViewModel(QObject):
    _log_message_sig = Signal(str)

    def __init__(self, parent=None):
        super(ViewModel, self).__init__(parent)
        self._log = LogMessage()
        self._clock = Clock()
        self._info = AppInfo()
        # Cards Components
        self._router_card = RouterCard()
        self._router_card.logger_signal.connect(self._log.update_message)
        self._dns_card = DNSCard()
        self._dns_card.logger_signal.connect(self._log.update_message)

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

    @Property(QObject, constant=True)
    def router_card(self):
        return self._router_card

    @Property(QObject, constant=True)
    def dns_card(self):
        return self._dns_card

    def log_message(self, msg):
        self._log_message_sig.emit(msg)
