from __future__ import annotations
from enum import IntEnum

from . import UPNP
from .. import SockUrl
from ...common import oneshot_str_hexhashing


class ServerInfo(object):
    __slots__ = 'name', 'pub_ip', 'local_ip', 'registration_port'

    def __init__(self, registration_port: int):
        self.name = 'Pynet.Server'
        self.registration_port = registration_port
        self.local_ip = '192.168.1.21'
        self.pub_ip = '176.136.251.178'

    def get_registration_url(self) -> SockUrl.Abc:
        return SockUrl.Remote(sock_type=SockUrl.SERVER, ip='*', port=self.registration_port)

    @staticmethod
    def get_alive_url(client: ClientInfo) -> SockUrl.Abc:
        return SockUrl.Remote(sock_type=SockUrl.CLIENT, ip=client.pub_ip, port=client.alive_port)


REGISTRATION_PORT = 28028
SERVER_INFO = ServerInfo(registration_port=REGISTRATION_PORT)


class ClientInfo(object):
    __slots__ = 'name', 'pub_ip', 'local_ip', 'alive_port', 'data_ports', 'id'

    def __init__(self, name: str, alive_port: int, data_ports: [int]):
        self.name = name
        self.pub_ip = ''
        self.local_ip = ''
        self.alive_port = alive_port
        self.data_ports = data_ports
        self.id = oneshot_str_hexhashing(self.name + str(self.pub_ip))

    def update_ip(self):
        self.pub_ip = UPNP.get_public_ip()
        self.local_ip = UPNP.get_local_ip()

    @staticmethod
    def get_registration_url() -> SockUrl.Abc:
        return SockUrl.Remote(sock_type=SockUrl.CLIENT, ip=SERVER_INFO.local_ip, port=SERVER_INFO.registration_port)

    def get_alive_url_for_client(self) -> SockUrl.Abc:
        return SockUrl.Remote(sock_type=SockUrl.SERVER, ip="*", port=self.alive_port)

    def get_alive_url_for_server(self) -> SockUrl.Abc:
        return SockUrl.Remote(sock_type=SockUrl.CLIENT, ip=self.local_ip, port=self.alive_port)

    def __str__(self):
        return f'ClientInfo({self.id},{self.name},{self.pub_ip},{self.alive_port},{self.data_ports})'


class ClientRequestRegistration(object):
    __slots__ = 'client'

    def __init__(self, client: ClientInfo):
        self.client = client

    def __str__(self):
        return f'ClientRequestRegistration({self.client})'


class ClientRegisteredEnum(IntEnum):
    NEW = 0
    UPDATED = 1


class ClientReplyRegistration(object):
    __slots__ = 'clients', 'result'

    def __init__(self, result: ClientRegisteredEnum, clients: ClientsRegistered):
        self.result = result
        self.clients = clients

    def __str__(self):
        return f'ClientReplyRegistration({self.result}, {self.clients})'


class ClientsRegistered(object):
    __slots__ = 'clients', 'cache'

    def __init__(self):
        self.clients = {}
        # self.cache = Cache('Pynet.Clients')

    def get(self, client_id: int):
        return self.clients[client_id] if self.has(client_id) else None

    def has(self, client_id: int):
        return True if client_id in self.clients else None

    def add(self, client: ClientInfo) -> ClientRegisteredEnum:
        res = ClientRegisteredEnum.NEW
        if self.has(client.id):
            res = ClientRegisteredEnum.UPDATED
        self.clients.update({client.id: client})
        # self.cache.data = self.clients
        # self.cache.save()
        return res

    def remove(self, client: ClientInfo) -> bool:
        if self.has(client.id):
            self.clients.pop(client.id)
            # self.cache.data = self.clients
            # self.cache.save()
            return True
        return False

    @property
    def count(self):
        return len(self.clients)
