from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ...utils.property import PROPERTY_CACHE
from ...utils import Property, PropertyMeta
from . import Card


class DNSInfo(QObject, metaclass=PropertyMeta):
    mapped_port = Property('')
    dns_server = Property(False)
    clients = Property(dict())
