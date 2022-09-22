from __future__ import annotations

from .. import Node, Sock, UPNP
from . import ClientRequestRegistration, ClientReplyRegistration, ClientInfo, ClientsRegistered


class Client(Node):
    requester_registration: Node.Requester
    replier_alive: Node.Replier

    def __init__(self, name: str):
        Node.__init__(self, name)
        self.info = ClientInfo(name, 28128, data_ports=[])
        self.requester_registration = self.new_requester(self.info.get_registration_url(), flags=[(Sock.Flags.rcv_timeout, 1000), ])
        self.clients = ClientsRegistered()

    def register(self) -> bool:
        self.info.update_public_ip()
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
