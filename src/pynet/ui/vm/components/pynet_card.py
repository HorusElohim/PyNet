from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ...utils import Property, PropertyMeta
from . import Card
from pynet.model.network.dns import Client, KeepAliveRequest, KeepAliveReply
from time import strftime, localtime, sleep
from pynet.model import Singleton


class PynetClient(Client, metaclass=Singleton):
    pass


PYNET_CLIENT = PynetClient('Pynet.Client')


class PynetInfo(QObject, metaclass=PropertyMeta):
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
        self.requester_status = "🔴"


class PynetCardWorkerSignals(QObject):
    log = Signal(str)
    info = Signal(PynetInfo)


class PynetCardWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = PynetCardWorkerSignals()
        self.pynet_info = PynetInfo()
        self.pynet_client = PYNET_CLIENT
        self.alive = True
        self.registration_required = True

    def run(self):
        self.signals.log.emit('Pynet client registration ...')
        self.pynet_client.update_ip()
        self.upnp_map_alive_port()
        self.pynet_client_registration()
        self.signals.info.emit(self.pynet_info)
        self.keep_alive_loop()

    def upnp_map_alive_port(self):
        res = self.pynet_client.upnp_map_alive_port()
        self.pynet_info.data_port = ','.join(self.pynet_client.info.data_ports)
        if res:
            self.pynet_info.alive_port = str(self.pynet_client.info.alive_port) + " 🟢"
        else:
            self.pynet_info.alive_port = "🔴"

    def pynet_client_registration(self):
        res = self.pynet_client.register()
        self.signals.log.emit(f'Pynet Server: {"Online" if res else "Offline"}')
        if res:
            self.pynet_info.clients = self.pynet_client.clients
            self.pynet_info.server_status = "🟢"
            self.pynet_info.n_clients = self.pynet_client.clients.count
            self.pynet_info.last_update = strftime("%H:%M:%S", localtime())
            self.registration_required = False
        else:
            self.pynet_info.failed()
            self.registration_required = True

        self.signals.info.emit(self.pynet_info)

    def keep_alive_loop(self):
        self.signals.log.emit('Starting keep_alive loop ...')
        error_counter = 0
        self.pynet_client.create_keep_alive_rep()

        while self.alive:
            if self.registration_required:
                sleep(1)
                self.signals.log.emit('Recontacting the PyNet Server')
                self.pynet_client_registration()
                sleep(0.1)
            else:
                msg = self.pynet_client.replier_alive.receive()
                if msg == self.pynet_client.Sock.RECV_ERROR:
                    error_counter += 1
                    self.pynet_info.failed()
                    if error_counter == 3:
                        self.registration_required = True
                        error_counter = 0
                else:
                    if isinstance(msg, KeepAliveRequest):
                        self.pynet_info.clients = msg.clients
                        self.pynet_info.last_update = strftime("%H:%M:%S", localtime())
                        self.pynet_info.delta_ms = msg.delta_ms()
                        res = self.pynet_client.replier_alive.send(KeepAliveReply())
                        self.pynet_info.alive_status = "🟢"
                    else:
                        self.signals.log.emit('keep_alive server sent something wrong')
                        self.pynet_info.failed()


class PynetCard(Card):
    info = Property(PynetInfo())

    def __init__(self, parent=None):
        Card.__init__(self, parent=parent)
        self.warning_state()
        self.worker = PynetCardWorker()
        self.already_started = False

    @Slot(PynetInfo)
    def pynet_info_slot(self, pynet_info: PynetInfo):
        self.info = pynet_info
        if self.info.server_status == "🟢":
            self.success_state()
        else:
            self.error_state()

    def discover(self):
        if not self.already_started:
            th_pool = QThreadPool.globalInstance()
            self.worker = PynetCardWorker()
            self.worker.signals.log.connect(self.log_message)
            self.worker.signals.info.connect(self.pynet_info_slot)
            th_pool.start(self.worker)
            self.logger_signal.emit('Pynet client registration ...')
            self.already_started = True

    def __del__(self):
        self.worker.alive = False
        super(PynetCard, self).__del__()
