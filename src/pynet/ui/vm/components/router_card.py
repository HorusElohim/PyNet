from ....model import UPNP
from ...utils import Property
from . import Card, CardStatus, CardWorker, Status, CardWorkerData

MAPPED_PORT = 28128


class RouterData(CardWorkerData):
    model = Property('-', save=True)
    local_ip = Property('-', save=True)
    public_ip = Property('-', save=True)
    status = Property(False)
    nat = Property('NAT: 🔴')
    sip = Property('SIP: 🔴')
    upnp = Property('MAP: 🔴')


class RouterCardWorker(CardWorker):
    def __init__(self):
        super().__init__(worker_data_type=RouterData)

    def task(self) -> CardStatus:
        self.signals.log.emit('Upnp router discovering ...')
        self.data.model = UPNP.device.model_name
        self.data.public_ip = UPNP.get_public_ip()
        self.data.local_ip = UPNP.get_local_ip()
        self.data.status = UPNP.get_status()
        nat, sip = UPNP.get_nat_sip()
        self.data.nat = f'NAT: {"🟢" if nat else "🔴"}'
        self.data.sip = f'SIP: {"🟢" if sip else "🔴"}'
        self.signals.log.emit('Upnp router discovering completed')
        status = CardStatus()
        status.status = Status.success
        return status


class RouterCard(Card):
    data = Property(RouterData())

    def __init__(self, parent=None):
        super().__init__(worker_type=RouterCardWorker, parent=parent)
