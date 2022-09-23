from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ...utils import Property, PropertyMeta
from . import Card
from pynet.model.network.dns import Client
from time import strftime, localtime


class PynetInfo(QObject, metaclass=PropertyMeta):
    alive_port = Property('')
    data_port = Property('')
    requester_status = Property('🔴')
    alive_status = Property('🔴')
    server_status = Property('🔴')
    client_status = Property('🔴')
    last_update = Property("00:00:00")
    n_clients = Property(0)
    clients = Property(dict())


class PynetCardWorkerSignals(QObject):
    log = Signal(str)
    info = Signal(PynetInfo)


class PynetCardWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = PynetCardWorkerSignals()
        self.pynet_info = PynetInfo()
        self.pynet_client = Client('Pynet.Client')
        self.alive = True

    def keep_alive_loop(self):
        while self.alive:
            msg = self.pynet_client.replier_alive.receive()
            self.pynet_client.replier_alive.send(msg)

    def run(self):
        self.signals.log.emit('Pynet client registration ...')
        self.pynet_client.update_ip()
        res = self.pynet_client.upnp_map_alive_port()
        if res:
            self.pynet_info.alive_port = str(self.pynet_client.info.alive_port) + " 🟢"
        else:
            self.pynet_info.alive_port = "🔴"
        self.pynet_info.requester_status = "🟢" if self.pynet_client.requester_status else "🔴"
        self.pynet_info.data_port = ','.join(self.pynet_client.info.data_ports)
        res = self.pynet_client.register()
        self.signals.log.emit(f'Pynet client: {res}')
        if res:
            self.pynet_info.clients = self.pynet_client.clients
            self.pynet_info.server_status = "🟢"
            self.pynet_info.n_clients = self.pynet_client.clients.count
            self.pynet_info.last_update = strftime("%H:%M:%S", localtime())
        self.signals.info.emit(self.pynet_info)

        self.keep_alive_loop()


class PynetCard(Card):
    info = Property(PynetInfo())

    def __init__(self, parent=None):
        Card.__init__(self, parent=parent)
        self.warning_state()
        self.worker = PynetCardWorker()

    @Slot(PynetInfo)
    def pynet_info_slot(self, pynet_info: PynetInfo):
        self.info = pynet_info
        if self.info.server_status == "🟢":
            self.success_state()
        else:
            self.error_state()

    def discover(self):
        th_pool = QThreadPool.globalInstance()
        self.worker = PynetCardWorker()
        self.worker.signals.log.connect(self.log_message)
        self.worker.signals.info.connect(self.pynet_info_slot)
        th_pool.start(self.worker)
        self.logger_signal.emit('Pynet client registration ...')
