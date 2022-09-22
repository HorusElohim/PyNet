from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ...utils import Property, PropertyMeta
from . import Card
from pynet.model.network.dns import Client


class DNSInfo(QObject, metaclass=PropertyMeta):
    mapped_port = Property(0)
    dns_server = Property('🔴')
    clients = Property(dict())
    n_clients = Property(0)


class DNSCardWorkerSignals(QObject):
    log = Signal(str)
    info = Signal(DNSInfo)


class DNSCardWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = DNSCardWorkerSignals()
        self.dns_info = DNSInfo()
        self.dns_client = Client('Pynet.Client')

    def run(self):
        self.signals.log.emit('DNS client registration ...')
        res = self.dns_client.register()
        self.signals.log.emit(f'DNS client: {res}')
        if res:
            self.dns_info.clients = self.dns_client.clients
            self.dns_info.dns_server = "🟢"
            self.dns_info.mapped_port = 28128
            self.dns_info.n_clients = self.dns_client.clients.count
        self.signals.info.emit(self.dns_info)


class DNSCard(Card):
    info = Property(DNSInfo())

    def __init__(self, parent=None):
        Card.__init__(self, parent=parent)
        self.warning_state()
        self.worker = DNSCardWorker()

    @Slot(DNSInfo)
    def dns_info_slot(self, dns_info: DNSInfo):
        self.info = dns_info
        if self.info.dns_server == "🟢":
            self.success_state()
        else:
            self.error_state()

    def discover(self):
        th_pool = QThreadPool.globalInstance()
        self.worker = DNSCardWorker()
        self.worker.signals.log.connect(self.log_message)
        self.worker.signals.info.connect(self.dns_info_slot)
        th_pool.start(self.worker)
        self.logger_signal.emit('DNS client registration ...')
