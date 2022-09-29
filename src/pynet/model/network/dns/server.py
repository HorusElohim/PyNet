from __future__ import annotations
from ... import DDict
from .. import Node
from . import URLS, HEARTBEAT_PORT, DNS_PORT


class Server(Node):
    def __init__(self, nat_ports=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hb_rep = self.new_heartbeat_replier(URLS.server.heartbeat)
        self.dns_rep = self.new_heartbeat_replier(URLS.server.dns)
        self.nodes = self.Nodes()
        if nat_ports:
            self.get_upnp().new_port_mapping(self.get_upnp().local_ip, HEARTBEAT_PORT, HEARTBEAT_PORT)
            self.get_upnp().new_port_mapping(self.get_upnp().local_ip, DNS_PORT, DNS_PORT)

    def loop(self):
        while self.dns_rep.is_open:
            req = self.dns_rep.receive()
            if isinstance(req, self.Info):
                self.nodes.update({req.id: req})
                self.dns_rep.send(self.nodes)
