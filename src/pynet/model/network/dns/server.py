from __future__ import annotations

from ... import Cache
from .. import Node
from . import DNS_SERVER_URL, DNS_SERVER_NAME, DNSRecord, DNSRequest, DNSReply


class DNSServer(Node):
    replier: Node.Replier
    clients: {str: DNSRecord}
    active: bool

    def __init__(self):
        Node.__init__(self, DNS_SERVER_NAME)
        self.replier = self.new_replier(DNS_SERVER_URL)
        self.cache = Cache(DNS_SERVER_NAME, logger_other=self)
        self.upnp = self.new_upnp()
        self._upnp_registration()
        self.clients = {}
        self._load_clients_cache()
        self.active = False
        self.log.debug('done *')

    def _upnp_registration(self):
        self.upnp.delete_port_mapping(self.upnp.get_local_ip(), DNS_SERVER_URL.port)
        return self.upnp.new_port_mapping(self.upnp.get_local_ip(), DNS_SERVER_URL.port, DNS_SERVER_URL.port)

    def _load_clients_cache(self):
        for name, record in self.cache.data.items():
            self.clients.update({name: record})

    def _save_clients_cache(self):
        self.cache.data = self.clients
        self.cache.save()

    def add_client(self, dns_request: DNSRecord):
        if dns_request.name in self.clients:
            self.log.debug(f'updating client : {dns_request} added')
        else:
            self.log.debug(f'new client: {dns_request} added')

        self.clients.update({dns_request.name: dns_request.url})

    def start(self):
        self.log.debug('starting...')
        self.active = True
        while self.active:
            self.replier.send(self.process(self.replier.receive()))

    def process(self, msg: object) -> object:
        self.log.debug(f'processing request: {msg}')
        reply = ''
        try:
            if isinstance(msg, DNSRequest):
                self.add_client(msg.record)
                reply = DNSReply(clients=self.clients)
            else:
                reply = "Unable to be process"
        except Exception as ex:
            reply = "Failure"
            self.log.error(f'Exception: {ex}')

        return reply
