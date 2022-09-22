from PySide6.QtCore import QObject, Signal, Slot
from ....utils import Property, PropertyMeta


class Card(QObject, metaclass=PropertyMeta):
    logger_signal = Signal(str)
    completed_signal = Signal(bool)

    image = Property('')
    color = Property('white')
    visible_body = Property(False)

    @Slot(str)
    def log_message(self, msg):
        self.logger_signal.emit(msg)

    def success_state(self):
        self.color = "#7CFC00"
        self.completed_signal.emit(True)

    def warning_state(self):
        self.color = "#FFFF00"
        self.completed_signal.emit(False)

    def error_state(self):
        self.color = "#DC143C"
        self.completed_signal.emit(False)
