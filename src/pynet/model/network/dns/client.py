from __future__ import annotations

from .. import Node
from . import URLS, HEARTBEAT_PORT, DNS_PORT


class Client(Node):
    def __init__(self, nat_ports=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hb_req = self.new_heartbeat_requester(URLS.client.heartbeat)
        self.dns_req = self.new_requester(URLS.client.dns)
        self.nodes: Node.Nodes = {}
        if nat_ports:
            self.get_upnp().new_port_mapping(self.get_upnp().local_ip, HEARTBEAT_PORT, HEARTBEAT_PORT)
            self.get_upnp().new_port_mapping(self.get_upnp().local_ip, DNS_PORT, DNS_PORT)

    def update_nodes(self):
        self.dns_req.send(self.info)
        reply = self.dns_req.receive()
        if isinstance(reply, self.Nodes):
            self.nodes = reply

    @property
    def connected(self):
        return self.hb_req.connected
