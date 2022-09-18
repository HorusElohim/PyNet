from PySide6.QtCore import QTimer, QObject, Signal, Slot
from . import LOG


class Drop(QObject):
    items = []

    @Slot(str)
    def output_path(self, path):
        LOG.log.debug(f'Path received: {path}')
        self.items.append(path)
