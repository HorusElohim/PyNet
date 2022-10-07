from __future__ import annotations
from .. import Node
from . import URLS, DNS_PORT, ReplyOk


class Server(Node):
    def __init__(self, nat_ports=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dns_rep = self.new_replier(URLS.server.dns, flags=[(self.Sock.Flags.rcv_timeout, 3000), (self.Sock.Flags.snd_timeout, 3000)])
        self.nodes: Node.Nodes = {}
        self.need_update: {int: bool} = {}
        if nat_ports:
            self.get_upnp().new_port_mapping(self.get_upnp().local_ip, DNS_PORT, DNS_PORT)

    def loop(self):
        while self.dns_rep.is_open:
            req = self.dns_rep.receive()
            # Add node info , send all nodes info
            if isinstance(req, self.Info):
                rep_msg = self.__process_node_msg(req)
                self.dns_rep.send(rep_msg)
            # Error no income data
            elif req == self.Sock.RECV_ERROR:
                self.log.info('No nodes in the network')
                self.nodes = {}

    def __process_node_msg(self, node_info: Node.Info):
        # Check if new node
        if node_info.id not in self.nodes:
            # Add
            self.nodes[node_info.id] = node_info
            self.need_update[node_info.id] = True
            self.log.info(f'new node: {node_info}')
            # New node, net should be notified to all
            if len(self.nodes) > 0:
                for nid, in self.nodes.keys():
                    self.need_update[nid] = True
        else:
            # Update nodes connected
            self.nodes.update({node_info.id: node_info})
        # Return Reply msg
        if self.need_update[node_info.id]:
            return self.nodes
        else:
            return ReplyOk()
