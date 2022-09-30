import abc

from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool
from enum import Enum
from ....utils import Property, PropertyMeta
from ....utils.property import PROPERTY_CACHE


class Status(Enum):
    warning = 'warning'
    success = 'success'
    failed = 'failed'


class CardStatus(QObject):
    status: Status

    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = Status.warning


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

    @Slot(CardStatus)
    def status_slot(self, status: CardStatus):
        print(type(status), status)
        completed = False
        # Warning State
        if status.status == Status.warning:
            self.color = "#FFFF00"
        # Success State
        elif status.status == Status.success:
            self.color = "#7CFC00"
            completed = True
        elif status.status == Status.failed:
            self.color = "#DC143C"
        # Emit completed signal
        self.completed_signal.emit(completed)

    @Slot(QObject)
    def data_slot(self, data: QObject):
        print(f'SLOT-DATA: {type(data)} - {data}')
        self.data = data
        PROPERTY_CACHE.save()

    @Slot(str)
    def log_message(self, msg):
        self.logger_signal.emit(msg)


class CardWorkerData(QObject, metaclass=PropertyMeta):
    pass


class CardWorker(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        status = Signal(CardStatus)
        data = Signal(CardWorkerData)

    def __init__(self, worker_data_type):
        # Init QRunnable
        super().__init__()
        self.signals = CardWorker.Signals()
        self.active = False
        self.status = CardStatus()
        self.data = worker_data_type()
        print(f"CardWorkerInit: status: {type(self.status)} - {self.status}")

    def run(self):
        self.signals.log.emit(f'Starting {self.__class__} worker')
        self.active = True
        while self.active:
            self.status = self.task()
            self.signals.status.emit(self.status)
            self.signals.data.emit(self.data)
            self.active = False

    @abc.abstractmethod
    def task(self) -> CardStatus:
        pass
