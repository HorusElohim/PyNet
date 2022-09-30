import abc

from PySide6.QtCore import QObject, Signal, QRunnable
from ....utils import Property, PropertyMeta
from .core import Status
import time


class WorkerData(QObject, metaclass=PropertyMeta):
    pass


class Worker(QRunnable):
    class Signals(QObject):
        log = Signal(str)
        status = Signal(Status)
        data = Signal(WorkerData)

    def __init__(self, worker_data_type, loop=False, hertz=1):
        # Init QRunnable
        super().__init__()
        self.signals = Worker.Signals()
        self.active = False
        self.status = Status()
        self.data = worker_data_type()
        self.loop = loop
        self.hertz = hertz

    def run(self):
        self.signals.log.emit(f'Starting {self.__class__} worker')
        self.active = True

        while self.active:
            self.status = self.task()
            self.signals.status.emit(self.status)
            self.signals.data.emit(self.data)

            # If loop is set continue , else exit from the loop
            if not self.loop:
                self.active = False
            else:
                time.sleep(1 / self.hertz)

    @abc.abstractmethod
    def task(self) -> Status:
        pass
