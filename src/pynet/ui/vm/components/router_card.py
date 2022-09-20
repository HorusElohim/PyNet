import upnpclient
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ...utils.property import PROPERTY_CACHE
from ...utils import Property, PropertyMeta
from . import Card


class RouterInfo(QObject, metaclass=PropertyMeta):
    model = Property('-', save=True)
    ip = Property('-', save=True)
    status = Property(False)
    nat = Property('NAT: 🔴')
    sip = Property('SIP: 🔴')


class Upnp(object):
    def __init__(self):
        self.device = None
        self.info = RouterInfo()

    def discover_router(self) -> RouterInfo:
        devices = upnpclient.discover()
        self.device = devices[0] if len(devices) > 0 else None
        self.info.model = self.device.model_name
        self.info.ip = self.get_ip()
        self.info.status = self.get_status()
        self.info.nat, self.info.sip = self.get_nat_sip()
        return self.info

    def get_ip(self):
        return self.device.WANIPConn1.GetExternalIPAddress()['NewExternalIPAddress'] if self.device else ''

    def get_status(self):
        if self.device:
            if 'Connected' in self.device.WANIPConn1.GetStatusInfo()["NewConnectionStatus"]:
                return True
        return False

    def get_nat_sip(self):
        if self.device:
            status = self.device.WANIPConn1.GetNATRSIPStatus()
            sip = f'SIP: {"🟢" if status["NewRSIPAvailable"] else "🔴"}'
            nat = f'NAT: {"🟢" if status["NewNATEnabled"] else "🔴"}'
            return nat, sip
        else:
            return "🔴", "🔴"


class RouterCardWorkerSignals(QObject):
    log = Signal(str)
    info = Signal(RouterInfo)


class RouterCardWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = RouterCardWorkerSignals()
        self.upnp = Upnp()

    def run(self) -> None:
        self.signals.log.emit('Upnp router discovering ...')
        self.upnp.discover_router()
        self.signals.log.emit('Upnp router discovering completed')
        self.signals.info.emit(self.upnp.info)


class RouterCard(Card):
    info = Property(RouterInfo())
    logger_sig = Signal(str)

    def __init__(self, parent=None):
        super(RouterCard, self).__init__(parent)
        self.worker = None
        self.color = "yellow"

    @Slot(str)
    def log(self, msg):
        self.logger_sig.emit(msg)

    @Slot(RouterInfo)
    def router_info_slot(self, ri: RouterInfo):
        self.info = ri
        if self.info.status:
            self.color = "green"
        PROPERTY_CACHE.save()

    def discover(self):
        th_pool = QThreadPool.globalInstance()
        self.color = "yellow"
        self.worker = RouterCardWorker()
        self.worker.signals.log.connect(self.log)
        self.worker.signals.info.connect(self.router_info_slot)
        th_pool.start(self.worker)
