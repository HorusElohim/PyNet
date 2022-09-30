from ... import DDict
from .. import Node

SERVER_IP = "192.168.1.14"
HEARTBEAT_PORT = 33000
DNS_PORT = 33100

URLS = DDict(
    server=DDict(
        dns=Node.Url.Remote(sock_type=Node.Url.SERVER, ip='*', port=DNS_PORT),
        heartbeat=Node.Url.Remote(sock_type=Node.Url.SERVER, ip='*', port=HEARTBEAT_PORT)
    ),
    client=DDict(
        dns=Node.Url.Remote(sock_type=Node.Url.CLIENT, ip=SERVER_IP, port=DNS_PORT),
        heartbeat=Node.Url.Remote(sock_type=Node.Url.CLIENT, ip=SERVER_IP, port=HEARTBEAT_PORT)
    )
)
