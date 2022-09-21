import upnpclient
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from .... import Upnp
from ...utils.property import PROPERTY_CACHE
from ...utils import Property, PropertyMeta
from . import Card


class RouterInfo(QObject, metaclass=PropertyMeta):
    model = Property('-', save=True)
    local_ip = Property('-', save=True)
    public_ip = Property('-', save=True)
    status = Property(False)
    nat = Property('NAT: 🔴')
    sip = Property('SIP: 🔴')


class UpnpBridge(Upnp):
    def __init__(self):
        Upnp.__init__(self, auto_discover=False)
        self.info = RouterInfo()

    def discover_router(self) -> RouterInfo:
        self.discover()
        self.info.model = self.device.model_name
        self.info.public_ip = self.get_public_ip()
        self.info.local_ip = self.get_local_ip()
        self.info.status = self.get_status()
        nat, sip = self.get_nat_sip()
        self.info.nat = f'NAT: {"🟢" if nat else "🔴"}'
        self.info.sip = f'SIP: {"🟢" if sip else "🔴"}'
        return self.info


class RouterCardWorkerSignals(QObject):
    log = Signal(str)
    info = Signal(RouterInfo)


class RouterCardWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = RouterCardWorkerSignals()
        self.upnp = UpnpBridge()

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
