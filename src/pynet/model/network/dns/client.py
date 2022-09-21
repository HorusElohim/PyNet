from __future__ import annotations

from .. import Node, Sock
from . import DNS_CLIENT_URL, DNSRecord, DNSRequest, DNSReply


class DNSClient(Node):
    requester: Node.Requester

    def __init__(self, name: str):
        Node.__init__(self, name)
        self.requester = self.new_requester(DNS_CLIENT_URL, flags=[(Sock.Flags.rcv_timeout, 1000), ])
        self.clients = {str: DNSRecord}

    def register(self) -> bool:
        self.requester.send(DNSRequest(self.entity_name, self.requester.sock_urls[0]))
        reply = self.requester.receive()
        if isinstance(reply, DNSReply):
            self.clients = reply.clients
            self.log.debug(f"received correctly list of dns clients: {self.clients}")
            return True
        else:
            self.log.error(f"dns reply error: {reply}")
            return False
