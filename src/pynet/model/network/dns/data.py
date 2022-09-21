from __future__ import annotations

from .. import SockUrl


# DNS_IP = "176.136.251.178"
DNS_IP = "192.168.1.21"
DNS_PORT = 33133

DNS_SERVER_NAME = 'DNS-Server'
DNS_SERVER_URL = SockUrl.Remote(sock_type=SockUrl.SERVER, ip='*', port=DNS_PORT)
DNS_CLIENT_URL = SockUrl.Remote(sock_type=SockUrl.CLIENT, ip=DNS_IP, port=DNS_PORT)


class DNSRecord(object):
    __slots__ = "url", "name"

    def __init__(self, name: str, url: SockUrl.Abc):
        self.name = name
        self.url = url

    def __str__(self):
        return f'{self.name} -> {self.url}'


class DNSRequest(object):
    __slots__ = 'record'

    def __init__(self, name: str, url: SockUrl.Abc):
        self.record = DNSRecord(name, url)

    def __str__(self):
        return f'DNSQuery: {self.record}'


class DNSReply(object):
    __slots__ = 'clients'

    def __init__(self, clients: {str: DNSRecord}):
        self.clients = clients
