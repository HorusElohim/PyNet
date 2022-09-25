from __future__ import annotations
import abc
from enum import Enum
from time import time_ns

from ... import oneshot_str_hexhashing, Cache

from .. import Node, UPNP


class SteadyNodeData(Node):
    __slots__ = 'nodes', '_socket_pair', 'cache'

    def __init__(self, name: str, url: Node.Url.Remote):
        super().__init__(name)
        self._socket_pair = self.new_pair(url)
        self._url = url
        self.cache = Cache(self.node_name)
        self.nodes = self.Nodes()

    class Info:
        class Status(Enum):
            disconnected = 0
            connected = 1

        __slots__ = 'name', 'pub_ip', 'local_ip', 'url', '_id', 'status', 'heartbeat_stamp', 'cache'

        def __init__(self, name, pub_ip, local_ip, url):
            self.name = name
            self.pub_ip = pub_ip
            self.local_ip = local_ip
            self.url = url
            self.status = self.Status.disconnected
            self.heartbeat_stamp = 0

        def __str__(self):
            return f'Node.Info({self.status}| {self.name}, {self.pub_ip}, {self.local_ip}, {self.id}, {self.url})'

        def touch_heartbeat(self):
            self.heartbeat_stamp = time_ns()

        @property
        def id(self):
            return oneshot_str_hexhashing(self.name + str(self.pub_ip))

        def connect(self):
            self.status = self.Status.connected

        def disconnect(self):
            self.status = self.Status.disconnected

    class Nodes(dict):
        __init__: {int: SteadyNodeData.Info}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __str__(self):
            return f'Nodes({self.__dict__})'

    class RegistrationRequest:
        __slots__ = 'info'

        def __str__(self):
            return f'RegistrationRequest({self.info})'

    class HeartBeatRequest:
        __slots__ = 'nodes'

        def __init__(self, nodes: SteadyNodeData.Nodes):
            self.nodes = nodes

        def __str__(self):
            return f'HeartBeatRequest({str(self.nodes)})'

    class HeartBeatReply:
        __slots__ = 'id', 'stamp'

        def __init__(self, node_id: int):
            self.id = node_id
            self.stamp = time_ns()

    @property
    def url(self):
        return self.Url.Remote(self.Url.SockType.opposite(self._url.sock_type), UPNP.get_local_ip(), self._url.port)

    @property
    def info(self):
        return self.Info(self.node_name, UPNP.pub_ip, UPNP.local_ip, self.url)

    @property
    def registration_request_message(self):
        msg = self.RegistrationRequest()
        msg.info = self.info
        return msg

    @property
    def heartbeat_reply_message(self):
        return self.HeartBeatReply(self.info.id)

    @property
    def heartbeat_request_message(self):
        return self.HeartBeatRequest(self.nodes)


class SteadyNodeBase(SteadyNodeData):

    def send(self, msg):
        self._socket_pair.send(msg)

    def recv(self, no_block=True):
        flag = 0
        if no_block:
            flag = self.Sock.Flags.no_block
        return self._socket_pair.receive(flag=self.Sock.Flags.no_block)

    @abc.abstractmethod
    def process_new_message(self, in_msg) -> object:
        pass
