from pynet import __version__
from PySide6.QtCore import QTimer, QObject, Signal, Property
from . import LOG


class Info(QObject):

    def __init__(self):
        super().__init__()
        self._name = "PyNet"
        self._version = __version__
        LOG.log.debug("constructed")

    def get_name(self):
        return self._name

    def get_version(self):
        return self._version

    name = Property(str, get_name)
    version = Property(str, get_version)
