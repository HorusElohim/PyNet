from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool
from enum import Enum
from ....utils import Property, PropertyMeta
from ....utils.property import PROPERTY_CACHE


class StatusEnum(Enum):
    warning = 'warning'
    success = 'success'
    failed = 'failed'


class Status(QObject):
    status: StatusEnum

    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = StatusEnum.warning


class Card(QObject, metaclass=PropertyMeta):
    logger_signal = Signal(str)
    completed_signal = Signal(bool)
    worker: QRunnable = None

    image = Property('')
    color = Property('white')
    visible_body = Property(False)

    def __init__(self, worker_type, parent=None):
        super().__init__(parent=parent)
        self.worker_type = worker_type
        self.worker = worker_type()
        self.worker.signals.log.connect(self.log_message)
        self.worker.signals.status.connect(self.status_slot)
        self.worker.signals.data.connect(self.data_slot)
        # Set processing state
        self.color = "gray"

    def start(self):
        th_pool = QThreadPool.globalInstance()
        th_pool.start(self.worker)

    @Slot(Status)
    def status_slot(self, status: Status):
        print(type(status), status)
        completed = False
        # Warning State
        if status.status == StatusEnum.warning:
            self.color = "#FFFF00"
        # Success State
        elif status.status == StatusEnum.success:
            self.color = "#7CFC00"
            completed = True
        elif status.status == StatusEnum.failed:
            self.color = "#DC143C"
        # Emit completed signal
        self.completed_signal.emit(completed)

    @Slot(QObject)
    def data_slot(self, data: QObject):
        self.data = data

    @Slot(str)
    def log_message(self, msg):
        self.logger_signal.emit(msg)

    def __del__(self):
        if self.worker:
            self.worker.active = False
