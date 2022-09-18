from PySide6.QtCore import QObject, Slot, Signal, Property
from .components import Clock, Info
from .. import LOG


class ViewModel(QObject):

    def __init__(self, parent=None):
        super(ViewModel, self).__init__(parent)
        self._clock = Clock()
        self._info = Info()
        LOG.log.debug("VM Constructed")

    def start(self):
        self.get_clock().start()
        LOG.log.debug('start')

    def get_clock(self):
        return self._clock

    def set_clock(self, val):
        self._clock = val

    @Signal
    def clock_updated(self):
        pass

    def get_info(self):
        return self._info

    # Properties exposed to QML
    clock = Property(Clock, get_clock, set_clock, notify=clock_updated)
    info = Property(Clock, get_info)
