from ...utils import Property, PropertyMeta
from pynet.model.network import dns
from time import strftime, localtime, sleep
from . import card


class DNSData(card.WorkerData):
    alive_port = Property('')
    data_port = Property('')
    heartbeat_status = Property(card.FAILED_STR)
    server_status = Property(card.FAILED_STR)
    client_status = Property(card.FAILED_STR)
    last_update = Property("00:00:00")
    ping_ms = Property(0)
    n_clients = Property(0)
    clients = Property(dict())

    def failed(self):
        self.server_status = card.FAILED_STR
        self.heartbeat_status = card.FAILED_STR
        self.client_status = card.FAILED_STR


class PynetCardWorker(card.Worker):
    def __init__(self):
        super().__init__(worker_data_type=DNSData, loop=True)
        self.dns_client = dns.Client(node_name='Pynet.DNS.Client')
        self.log_once = True
        self.retry_count = 0

    def task(self):
        status = card.Status()
        if self.dns_client.update_nodes():
            self.retry_count = 0
            # Ping
            self.data.ping_ms = self.dns_client.ping
            # Update Last update
            self.data.server_status = card.SUCCESS_STR
            self.data.last_update = strftime("%H:%M:%S", localtime())
            # Ping time
            # DNS Status
            self.data.server_status = card.SUCCESS_STR
            # Nodes
            self.data.nodes = self.dns_client.nodes
            self.data.n_clients = len(self.dns_client.nodes)
            if self.log_once:
                self.signals.log.emit('Connected to Pynet DNS Server')
                self.log_once = False
            status.status = card.StatusEnum.success
        else:
            self.retry_count += 1
            self.data.server_status = card.FAILED_STR
            self.signals.log.emit(f'Pynet DNS Server lost. Retry {self.retry_count}')
            status.status = card.StatusEnum.failed
        return status


class PynetCard(card.Card):
    data = Property(DNSData())

    def __init__(self, parent=None):
        super().__init__(worker_type=PynetCardWorker, parent=parent)
