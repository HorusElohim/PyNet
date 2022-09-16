from PySide6.QtCore import QTimer, QObject, Signal, Slot
from . import CTRL_LOGGER


class Drop(QObject):
    items = []

    @Slot(str)
    def output_path(self, path):
        CTRL_LOGGER.log.debug(f'Path received: {path}')
        self.items.append(path)
