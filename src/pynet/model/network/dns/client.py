from __future__ import annotations

from .. import Node
from . import DNS_CLIENT_URL, DNSRecord, DNSRequest, DNSReply


class DNSClient(Node):
    requester: Node.Requester

    def __init__(self, name: str):
        Node.__init__(self, name)
        self.requester = self.new_requester(DNS_CLIENT_URL)
        self.clients = {str: DNSRecord}
        self.upnp = Node.Upnp()

    def register(self) -> bool:
        self.requester.send(DNSRequest(self.entity_name, self.requester.sock_urls[0]))
        reply = self.requester.receive()
        if isinstance(reply, DNSReply):
            self.clients = reply.clients
            self.log.debug("received correctly list of dns clients ")
        else:
            self.log.error(f"dns reply error: {reply}")
        