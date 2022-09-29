from __future__ import annotations

import time

from .. import Node
from . import URLS, DNS_PORT


class Client(Node):
    def __init__(self, nat_ports=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dns_req = self.new_requester(URLS.client.dns, flags=[(self.Sock.Flags.rcv_timeout, 3000), (self.Sock.Flags.snd_timeout, 3000)])
        self.nodes: Node.Nodes = {}
        self.dns_nat_port = False
        self.connected = False
        self.ping = 0
        if nat_ports:
            self.dns_nat_port = self.get_upnp().new_port_mapping(self.get_upnp().local_ip, DNS_PORT, DNS_PORT)

    def update_nodes(self):
        s = time.time_ns()
        self.dns_req.send(self.info)
        reply = self.dns_req.receive()
        self.ping = (time.time_ns() - s) * 1e-6

        if isinstance(reply, dict):
            self.nodes = reply
            self.connected = True
            return True

        self.connected = False
        return False
