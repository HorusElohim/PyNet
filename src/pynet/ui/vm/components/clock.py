from PySide6.QtCore import QTimer, QObject, Signal, Property
from time import strftime, localtime
from . import LOG


class Clock(QObject):
    time_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._time = "00:00:00"

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs 100
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        LOG.log.debug('CTRL-Clock constructed')

    def update_time(self):
        # Pass the current time to QML.
        self._time = strftime("%H:%M:%S", localtime())
        self.time_changed.emit(self.get_time())

    def get_time(self):
        return self._time

    def set_time(self, val):
        self._time = val

    time = Property(str, get_time, set_time, notify=time_changed)
