from PySide6.QtCore import Property, QObject, Signal, QRunnable, Slot, QThreadPool
import upnpclient

from . import Cache


class Router(QObject):
    model_sig = Signal(str)
    status_sig = Signal(str)
    ip_sig = Signal(str)
    nat_sig = Signal(str)
    sip_sig = Signal(str)

    def __init__(self):
        super(Router, self).__init__()
        self.cache = Cache('upnp.Router')
        self.model: str = self.cache.get('model')
        self.status: str = "Connection: 🔴"
        self.ip: str = self.cache.get('ip')
        self.nat: str = "Nat: 🔴"
        self.sip: str = "Sip: 🔴"

    @Property(str, notify=model_sig)
    def model(self):
        return self._model

    @model.setter
    def model(self, m):
        self._model = m
        self.model_sig.emit(m)

    @Property(str, notify=status_sig)
    def status(self):
        return self._status

    @status.setter
    def status(self, m):
        self._status = m

    @Property(str, notify=ip_sig)
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, m):
        self._ip = m

    @Property(str, notify=nat_sig)
    def nat(self):
        return self._nat

    @nat.setter
    def nat(self, m):
        self._nat = m

    @Property(str, notify=sip_sig)
    def sip(self):
        return self._sip

    @sip.setter
    def sip(self, m):
        self._sip = m

    def save(self):
        self.cache.data = dict(model=self._model,
                               ip=self._ip)
        self.cache.save()


class UpnpDiscoverySignals(QObject):
    log = Signal(str)
    router = Signal(QObject)


class UpnpDiscoveryWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = UpnpDiscoverySignals()
        self.router = Router()

    def run(self):
        self.signals.log.emit('start router discovery...')
        devices = upnpclient.discover()

        if len(devices) > 0:
            d = devices[0]
            self.router.model = d.model_name
            ip = d.WANIPConn1.GetExternalIPAddress()
            if 'NewExternalIPAddress' in ip:
                self.router.ip = ip['NewExternalIPAddress']

            status = d.WANIPConn1.GetStatusInfo()
            if 'NewConnectionStatus' in status:
                self.router.status = f'Connection: {"🟢" if status["NewConnectionStatus"] == "Connected" else "🔴"}'
            status = d.WANIPConn1.GetNATRSIPStatus()
            if 'NewRSIPAvailable' in status:
                self.router.sip = f'sip: {"🟢" if status["NewRSIPAvailable"] else "🔴"}'
            if 'NewNATEnabled' in status:
                self.router.nat = status['NewNATEnabled']
                self.router.nat = f'Nat: {"🟢" if status["NewNATEnabled"] else "🔴"}'
            self.signals.log.emit(f'router info updated')
            self.signals.router.emit(self.router)


class UpnpClient(QObject):
    log_msg_sig = Signal(str)
    router_sig = Signal(QObject)

    def __init__(self, parent=None):
        super(UpnpClient, self).__init__(parent)
        self.devices = None
        self._router = Router()
        self.cache = Cache('UpnpClient.Router')
        # self.router
        self.worker = None

    @Property(QObject, notify=router_sig)
    def router(self):
        return self._router

    @router.setter
    def router(self, r):
        self._router = r
        self.router_sig.emit(self._router)

    @Slot(str)
    def log(self, msg):
        self.log_msg_sig.emit(msg)

    @Slot(QObject)
    def router_slot(self, r):
        self.router = r
        self.router.save()

    def start_discovery(self):
        th_pool = QThreadPool.globalInstance()
        self.worker = UpnpDiscoveryWorker()
        self.worker.signals.log.connect(self.log)
        self.worker.signals.router.connect(self.router_slot)
        th_pool.start(self.worker)
