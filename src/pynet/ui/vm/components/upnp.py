from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool
import upnpclient
from ...utils import Property, PropertyMeta
from ...utils.property import PROPERTY_CACHE


class Router(QObject, metaclass=PropertyMeta):
    model = Property('-', save=True)
    status = Property('Connection: 🔴')
    ip = Property('-', save=True)
    nat = Property('NAT: 🔴')
    sip = Property('SIP: 🔴')


class UpnpDiscoverySignals(QObject):
    log = Signal(str)
    router = Signal(QObject)


class UpnpDiscoveryWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = UpnpDiscoverySignals()
        self.router = Router()

    @staticmethod
    def get_ip(device):
        return device.WANIPConn1.GetExternalIPAddress()['NewExternalIPAddress']

    @staticmethod
    def get_status(device):
        return f'Connection: {"🟢" if device.WANIPConn1.GetStatusInfo()["NewConnectionStatus"] == "Connected" else "🔴"}'

    @staticmethod
    def get_nat_sip(device):
        status = device.WANIPConn1.GetNATRSIPStatus()
        sip = f'SIP: {"🟢" if status["NewRSIPAvailable"] else "🔴"}'
        nat = f'NAT: {"🟢" if status["NewNATEnabled"] else "🔴"}'
        return nat, sip

    def run(self):
        self.signals.log.emit('start router discovery...')
        devices = upnpclient.discover()

        if len(devices) > 0:
            d = devices[0]
            self.router.model = d.model_name
            self.router.ip = self.get_ip(d)
            self.router.status = self.get_status(d)
            self.router.nat, self.router.sip = self.get_nat_sip(d)
            self.signals.log.emit(f'router info updated')
            self.signals.router.emit(self.router)


class UpnpClient(QObject, metaclass=PropertyMeta):
    router = Property(Router())
    logger_signal = Signal(str)

    def __init__(self, parent=None):
        super(UpnpClient, self).__init__(parent)
        self.devices = None
        self.worker = None

    @Slot(str)
    def log(self, msg):
        self.logger_signal.emit(msg)

    @Slot(QObject)
    def router_slot(self, r):
        self.router = r
        PROPERTY_CACHE.save()

    def start_discovery(self):
        th_pool = QThreadPool.globalInstance()
        self.worker = UpnpDiscoveryWorker()
        self.worker.signals.log.connect(self.log)
        self.worker.signals.router.connect(self.router_slot)
        th_pool.start(self.worker)
