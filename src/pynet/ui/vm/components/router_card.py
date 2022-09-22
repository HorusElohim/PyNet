from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool, QCoreApplication

from ....model import UPNP
from ...utils.property import PROPERTY_CACHE
from ...utils import Property, PropertyMeta
from . import Card

MAPPED_PORT = 28128


class RouterInfo(QObject, metaclass=PropertyMeta):
    model = Property('-', save=True)
    local_ip = Property('-', save=True)
    public_ip = Property('-', save=True)
    status = Property(False)
    nat = Property('NAT: 🔴')
    sip = Property('SIP: 🔴')
    upnp = Property('MAP: 🔴')


class UpnpBridge:
    def __init__(self):
        self.info = RouterInfo()

    def discover_router(self) -> RouterInfo:
        if UPNP.device is None:
            UPNP.discover()
        self.info.model = UPNP.device.model_name
        self.info.public_ip = UPNP.get_public_ip()
        self.info.local_ip = UPNP.get_local_ip()
        self.info.status = UPNP.get_status()
        nat, sip = UPNP.get_nat_sip()
        self.info.nat = f'NAT: {"🟢" if nat else "🔴"}'
        self.info.sip = f'SIP: {"🟢" if sip else "🔴"}'
        # Mapping
        res = UPNP.new_port_mapping(self.info.local_ip, MAPPED_PORT, MAPPED_PORT)
        self.info.upnp = f'MAP: {"🟢" if res else "🔴"}'
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

    def __init__(self, parent=None):
        super(RouterCard, self).__init__(parent)
        self.worker = None
        self.warning_state()

    @Slot(RouterInfo)
    def router_info_slot(self, ri: RouterInfo):
        self.info = ri
        if self.info.status:
            self.success_state()
        else:
            self.error_state()
        PROPERTY_CACHE.save()

    def discover(self):
        th_pool = QThreadPool.globalInstance()
        self.worker = RouterCardWorker()
        self.worker.signals.log.connect(self.log_message)
        self.worker.signals.info.connect(self.router_info_slot)
        th_pool.start(self.worker)
