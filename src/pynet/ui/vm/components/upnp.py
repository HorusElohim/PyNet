from PySide6.QtCore import Property, QObject, Signal, QRunnable, Slot, QThreadPool
import upnpclient
from dataclasses import dataclass


@dataclass
class Router:
    model: str
    desc: str
    nat: bool


class UpnpDiscoverySignals(QObject):
    log = Signal(str)
    ip = Signal(str)
    router = Signal(str)
    available = Signal(bool)


class UpnpDiscoveryWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = UpnpDiscoverySignals()

    def run(self):
        self.signals.log.emit('start upnp discovery...')
        devices = upnpclient.discover()
        self.signals.log.emit('upnp discovery done')
        if len(devices) > 0:
            d = devices[0]
            self.signals.log.emit('router model discovery...')
            d.model_name
            self.signals.log.emit('public ip discovery...')
            ip = d.WANIPConn1.GetExternalIPAddress()
            if 'NewExternalIPAddress' in ip:
                ip = ip['NewExternalIPAddress']
                self.signals.ip.emit(ip)
                self.signals.log.emit(f'public ip updated')


class UpnpClient(QObject):
    log_msg_sig = Signal(str)
    ip_sig = Signal(str)
    router_sig = Signal(str)

    def __init__(self, parent=None):
        super(UpnpClient, self).__init__(parent)
        self.devices = None
        self._ip = "undefined"
        self._router = "undefined"

    @Property(str, notify=ip_sig)
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, v):
        self._ip = v
        self.ip_sig.emit(self._ip)

    @Property(str, notify=router_sig)
    def router(self):
        return self._router

    @router.setter
    def router(self, v):
        self._router = v
        self.router_sig.emit(self._router)

    @Slot(str)
    def log(self, msg):
        self.log_msg_sig.emit(msg)

    @Slot(str)
    def ip_slot(self, ip):
        self.ip = ip

    def start_discovery(self):
        th_pool = QThreadPool.globalInstance()
        w = UpnpDiscoveryWorker()
        w.signals.log.connect(self.log)
        w.signals.ip.connect(self.ip_slot)
        w.signals.router.connect(self.ip_slot)
        th_pool.start(w)
