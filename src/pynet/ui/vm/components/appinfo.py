from pynet import __version__
from PySide6.QtCore import QTimer, QObject, Signal, Property
from . import LOG


class AppInfo(QObject):

    def __init__(self):
        super().__init__()
        self._name = "PyNet"
        self._version = __version__
        LOG.log.debug("constructed")

    @Property(str, constant=True)
    def name(self):
        return self._name

    @Property(str, constant=True)
    def version(self):
        return self._version
