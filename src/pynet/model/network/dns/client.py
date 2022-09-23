from __future__ import annotations

from .. import Node, Sock, UPNP
from . import ClientRequestRegistration, ClientReplyRegistration, ClientInfo, ClientsRegistered, KeepAliveReply, KeepAliveRequest


class Client(Node):
    requester_registration: Node.Requester
    replier_alive: Node.Replier

    def __init__(self, name: str):
        Node.__init__(self, name)
        self.info = ClientInfo(name=name, alive_port=28128, data_ports=[])
        self.requester_registration = self.new_requester(self.info.get_registration_url(), flags=[(Sock.Flags.rcv_timeout, 3000), ])
        self.clients = ClientsRegistered()
        self.replier_alive = self.new_replier(self.info.get_alive_url_for_client(), flags=[(self.Sock.Flags.rcv_timeout, 3000)])
        self.alive = True

    def update_ip(self):
        self.info.update_ip()

    def register(self) -> bool:
        self.requester_registration.send(ClientRequestRegistration(self.info))
        reply = self.requester_registration.receive()
        self.log.debug(f"received: {reply}")
        if isinstance(reply, ClientReplyRegistration):
            self.clients = reply.clients
            self.log.debug(f"received correctly list of clients: {self.clients}")
            return True
        else:
            self.log.error(f"pynet-server reply error: {reply}")
            return False

    def upnp_map_alive_port(self):
        return self.get_upnp().new_port_mapping(self.info.local_ip, self.info.alive_port, self.info.alive_port)

    def _keep_alive_loop(self):
        self.log.debug("starting keep_alive loop")
        while self.alive:
            msg = self.replier_alive.receive()
            if msg == self.Sock.RECV_ERROR:
                self.log.error('keep_alive client receive ERROR')
            if isinstance(msg, KeepAliveRequest):
                self.clients = msg.clients
                res = self.replier_alive.send(KeepAliveReply())
                if not res:
                    self.log.error('keep_alive client sent ERROR')
            else:
                self.log.error('keep_alive server sent something wrong')
