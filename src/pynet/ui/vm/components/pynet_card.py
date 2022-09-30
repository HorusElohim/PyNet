from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ...utils import Property, PropertyMeta
from . import Card
from pynet.model.network import dns
from time import strftime, localtime, sleep

SUCCESS = "🟢"
FAILED = "🔴"
STATUS = lambda x: SUCCESS if x else FAILED


class DNSInfo(QObject, metaclass=PropertyMeta):
    alive_port = Property('')
    data_port = Property('')
    heartbeat_status = Property(FAILED)
    server_status = Property(FAILED)
    client_status = Property(FAILED)
    last_update = Property("00:00:00")
    ping_ms = Property(0)
    n_clients = Property(0)
    clients = Property(dict())

    def failed(self):
        self.server_status = FAILED
        self.heartbeat_status = FAILED
        self.client_status = FAILED


class PynetCardWorkerSignals(QObject):
    log = Signal(str)
    info = Signal(DNSInfo)


class PynetCardWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = PynetCardWorkerSignals()
        self.dns_info = DNSInfo()
        self.dns_client = dns.Client(node_name='Pynet.DNS.Client')
        self.active = True
        self.log_once = True
        self.retry_count = 0

    def run(self):
        self.signals.log.emit('Pynet DNS registration ...')
        self.signals.info.emit(self.dns_info)
        sleep(1)
        self.loop()

    def loop(self):
        self.signals.log.emit('Contacting the Pynet DNS Server ... ')

        while self.active:
            sleep(1)
            # Todo Set Warning state
            # Todo Add signal/slot for state and remove Info
            # Ask for all the nodes connected
            if self.dns_client.update_nodes():
                self.retry_count = 0
                # Ping
                self.dns_info.ping_ms = self.dns_client.ping
                # Update Last update
                self.dns_info.server_status = SUCCESS
                self.dns_info.last_update = strftime("%H:%M:%S", localtime())
                # Ping time
                # DNS Status
                self.dns_info.server_status = SUCCESS
                # Nodes
                self.dns_info.nodes = self.dns_client.nodes
                self.dns_info.n_clients = len(self.dns_client.nodes)
                if self.log_once:
                    self.signals.log.emit('Connected to Pynet DNS Server')
                    self.log_once = False
            else:
                self.retry_count += 1
                self.dns_info.server_status = FAILED
                self.signals.log.emit(f'Pynet DNS Server lost. Retry {self.retry_count}')

            self.signals.info.emit(self.dns_info)


class PynetCard(Card):
    info = Property(DNSInfo())

    def __init__(self, parent=None):
        Card.__init__(self, parent)
        self.warning_state()
        self.worker = PynetCardWorker()
        self.already_started = False

    @Slot(DNSInfo)
    def info_slot(self, info: DNSInfo):
        self.info = info
        if self.info.server_status == SUCCESS:
            self.success_state()
        else:
            self.error_state()

    def discover(self):
        if not self.already_started:
            th_pool = QThreadPool.globalInstance()
            self.worker = PynetCardWorker()
            self.worker.signals.log.connect(self.log_message)
            self.worker.signals.info.connect(self.info_slot)
            th_pool.start(self.worker)
            self.logger_signal.emit('Pynet client registration ...')
            self.already_started = True

    def __del__(self):
        self.worker.active = False
