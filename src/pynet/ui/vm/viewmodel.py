from PySide6.QtCore import QObject, Slot, Signal, Property
from .components import Clock, AppInfo, LogMessage, RouterCard, PynetCard
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
        self._router_card.completed_signal.connect(self.router_completed_slot)
        self._pynet_card = PynetCard()
        self._pynet_card.logger_signal.connect(self._log.update_message)
        ##################
        self._log_message_sig.connect(self._log.update_message)
        LOG.log.debug("VM Constructed")

    def start(self):
        self._router_card.visible_body = True
        self._router_card.start()

    @Slot(bool)
    def router_completed_slot(self, val):
        if val:
            self._pynet_card.visible_body = True
            self._pynet_card.start()
        else:
            self._pynet_card.visible_body = False
        print(f'router completed: {val}')

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
    def pynet_card(self):
        return self._pynet_card

    def log_message(self, msg):
        self._log_message_sig.emit(msg)
