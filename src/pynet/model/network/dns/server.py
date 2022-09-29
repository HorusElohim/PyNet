from __future__ import annotations
from .. import Node
from . import URLS, DNS_PORT


class Server(Node):
    def __init__(self, nat_ports=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dns_rep = self.new_replier(URLS.server.dns, flags=[(self.Sock.Flags.rcv_timeout, 3000), (self.Sock.Flags.snd_timeout, 3000)])
        self.nodes: Node.Nodes = {}
        if nat_ports:
            self.get_upnp().new_port_mapping(self.get_upnp().local_ip, DNS_PORT, DNS_PORT)

    def loop(self):
        while self.dns_rep.is_open:
            req = self.dns_rep.receive()
            # Add node info , send all nodes info
            if isinstance(req, self.Info):
                self.nodes.update({req.id: req})
                self.dns_rep.send(self.nodes)
            # Error no income data
            elif req == self.Sock.RECV_ERROR:
                self.nodes = {}
