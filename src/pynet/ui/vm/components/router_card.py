from ....model import UPNP
from ...utils import Property
from ...utils.property import PROPERTY_CACHE
from . import card


class RouterData(card.WorkerData):
    model = Property('-', save=True)
    local_ip = Property('-', save=True)
    public_ip = Property('-', save=True)
    status = Property(False)
    nat = Property('NAT: 🔴')
    sip = Property('SIP: 🔴')
    upnp = Property('MAP: 🔴')


class RouterCardWorker(card.Worker):
    def __init__(self):
        super().__init__(worker_data_type=RouterData)

    def task(self) -> card.Status:
        self.signals.log.emit('Upnp router discovering ...')
        self.data.model = UPNP.device.model_name
        self.data.public_ip = UPNP.get_public_ip()
        self.data.local_ip = UPNP.get_local_ip()
        self.data.status = UPNP.get_status()
        nat, sip = UPNP.get_nat_sip()
        self.data.nat = f'NAT: {card.status_str(nat)}'
        self.data.sip = f'SIP: {card.status_str(sip)}'
        self.signals.log.emit('Upnp router discovering completed')
        status = card.Status()
        status.status = card.StatusEnum.success
        PROPERTY_CACHE.save()
        return status


class RouterCard(card.Card):
    data = Property(RouterData())

    def __init__(self, parent=None):
        super().__init__(worker_type=RouterCardWorker, parent=parent)
