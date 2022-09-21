from PySide6.QtCore import QObject, Signal, Slot
from ....utils import Property, PropertyMeta


class Card(QObject, metaclass=PropertyMeta):
    logger_signal = Signal(str)
    image = Property('')
    color = Property('white')
    visible_body = Property(True)

    @Slot(str)
    def log_message(self, msg):
        self.logger_signal.emit(msg)

    def success_state(self):
        self.color = "#7CFC00"

    def warning_state(self):
        self.color = "#FFFF00"

    def error_state(self):
        self.color = "#DC143C"
