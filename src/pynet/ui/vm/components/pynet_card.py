from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ...utils import Property, PropertyMeta
from . import Card
from pynet.model.network import dns
from time import strftime, localtime, sleep


class DNSInfo(QObject, metaclass=PropertyMeta):
    alive_port = Property('')
    data_port = Property('')
    alive_status = Property('🔴')
    server_status = Property('🔴')
    client_status = Property('🔴')
    last_update = Property("00:00:00")
    delta_ms = Property(0)
    n_clients = Property(0)
    clients = Property(dict())

    def failed(self):
        self.server_status = "🔴"
        self.alive_status = "🔴"
        self.alive_status = "🔴"


class PynetCardWorkerSignals(QObject):
    log = Signal(str)
    info = Signal(DNSInfo)


class PynetCardWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = PynetCardWorkerSignals()
        self.dns_info = DNSInfo()
        self.dns_client = dns.Client('Pynet-DNS-Client')
        self.registration_required = True

    def run(self):
        self.signals.log.emit('Pynet client registration ...')
        self.signals.info.emit(self.dns_info)
        sleep(1)
        self.keep_alive_loop()

    def upnp_map_alive_port(self):
        res = self.pynet_client.upnp_map_alive_port()
        self.dns_info.data_port = ','.join(self.pynet_client.dns_info.data_ports)
        if res:
            self.dns_info.alive_port = str(self.pynet_client.dns_info.alive_port) + " 🟢"
        else:
            self.dns_info.alive_port = "🔴"

    def keep_alive_loop(self):
        self.signals.log.emit('Starting client dns loop ...')
        error_counter = 0

        while self.dns_client.connected:
            # Ask all nodes connected
            self.dns_client.update_nodes()

            if self.registration_required:

                self.signals.log.emit('Recontacting the PyNet Server')
                self.pynet_client_registration()
                sleep(0.1)
            else:
                msg = self.pynet_client.replier_alive.receive()
                if msg == self.pynet_client.Sock.RECV_ERROR:
                    error_counter += 1
                    self.dns_info.failed()
                    if error_counter == 3:
                        self.registration_required = True
                        error_counter = 0
                else:
                    if isinstance(msg, KeepAliveRequest):
                        self.dns_info.clients = msg.clients
                        self.dns_info.last_update = strftime("%H:%M:%S", localtime())
                        self.dns_info.delta_ms = msg.delta_ms()
                        res = self.pynet_client.replier_alive.send(KeepAliveReply())
                        self.dns_info.alive_status = "🟢"
                    else:
                        self.signals.log.emit('keep_alive server sent something wrong')
                        self.dns_info.failed()


class PynetCard(Card):
    info = Property(DNSInfo())

    def __init__(self, parent=None):
        Card.__init__(self, parent=parent)
        self.warning_state()
        self.worker = PynetCardWorker()
        self.already_started = False

    @Slot(DNSInfo)
    def info_slot(self, info: DNSInfo):
        self.info = info
        if self.info.server_status == "🟢":
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
        self.worker.alive = False
        super(PynetCard, self).__del__()
