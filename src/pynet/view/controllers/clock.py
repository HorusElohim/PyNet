from PySide6.QtCore import QTimer, QObject, Signal
from time import strftime, localtime
from . import CTRL_LOGGER


class Clock(QObject):
    updated = Signal(str, arguments=['clockTime'])

    def __init__(self):
        super().__init__()

        # Define timer.
        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs 100 = 1/10th sec
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        CTRL_LOGGER.log.debug('CTRL-Clock constructed')

    def update_time(self):
        # Pass the current time to QML.
        curr_time = strftime("%H:%M:%S", localtime())
        self.updated.emit(curr_time)
