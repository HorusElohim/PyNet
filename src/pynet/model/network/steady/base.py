from __future__ import annotations

import abc
from enum import Enum
from time import time_ns

from ... import oneshot_str_hexhashing

from .. import Node, UPNP


class Nodes:
    __slots__ = '_nodes'

    def __init__(self):
        self._nodes: {int, SteadyNodeBase.Info} = {}

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, node_id: int) -> SteadyNodeBase.info:
        return self._nodes[node_id]

    def __setitem__(self, node_id: int, node_info: SteadyNodeBase.Info):
        self._nodes[node_id] = node_info

    def __delitem__(self, node_id):
        del self._nodes[node_id]

    def __iter__(self):
        return iter(self._nodes)


class SteadyNodeBase(Node):
    _socket_pair: Node.Pair | None

    def __init__(self, name: str, url: Node.Url.Remote):
        super().__init__(name)
        self._socket_pair = self.new_pair(url)
        self._url = url
        self.nodes = Nodes()
        self.output_buffer = []

    class Info:

        class Status(Enum):
            disconnected = 0
            connected = 1

        __slots__ = 'name', 'pub_ip', 'local_ip', 'url', '_id', 'status', 'heartbeat'

        def __init__(self, name, pub_ip, local_ip, url):
            self.name = name
            self.pub_ip = pub_ip
            self.local_ip = local_ip
            self.url = url
            self.status = self.Status.disconnected
            self.heartbeat = SteadyNodeBase.HeartBeat(self.id)

        def __str__(self):
            return f'Node.Info({self.status}| {self.name}, {self.pub_ip}, {self.local_ip}, {self.id}, {self.url})'

        @property
        def id(self):
            return oneshot_str_hexhashing(self.name + str(self.pub_ip))

        def connect(self):
            self.status = self.Status.connected

        def disconnect(self):
            self.status = self.Status.disconnected

        def touch_heartbeat(self):
            self.heartbeat = SteadyNodeBase.HeartBeat(self.id)

    class RegistrationRequest:
        __slots__ = 'info'

    class HeartBeat:
        __slots__ = 'id', 'stamp'

        def __init__(self, node_id: int):
            self.id = node_id
            self.stamp = time_ns()

    @property
    def url(self):
        return self.Url.Remote(self.Url.SockType.opposite(self._url.sock_type), UPNP.get_local_ip(), self._url.port)

    @property
    def info(self):
        return self.Info(self.node_name, UPNP.get_public_ip(), UPNP.get_local_ip(), self.url)

    @property
    def registration_request_message(self):
        msg = self.RegistrationRequest()
        msg.info = self.info
        return msg

    @abc.abstractmethod
    def process_message(self, in_msg) -> object:
        pass

    def _process_heartbeat(self, msg: HeartBeat):
        # Check heartbeat between thresholds
        last = self.nodes[msg.id].heartbeat
        stamp_diff = (msg.stamp - last.stamp) * 1e-9
        self.nodes[msg.id].heartbeat = msg
        # delta diff too high
        if stamp_diff > 1.5:
            self.log.warning(f'Heartbeat from: {msg.id} too high {stamp_diff}')

    def _process_registration(self, msg: RegistrationRequest):
        if msg.info.id in self.nodes:
            self.log.debug('received node registration of already connected node')
        else:
            self.log.debug(f'new node request registration: {msg.info}')
            # Reply with a registration request
            self.registration()
        # Update to connected and update heartbeat
        msg.info.connect()
        msg.info.touch_heartbeat()
        # Update the connected nodes
        self.nodes[msg.info.id] = msg.info

    def registration(self):
        # Add to the output buffer a registration message
        self.output_buffer.append(self.registration_request_message)

    def process_communications(self):
        while True:
            msg = self._socket_pair.receive(flag=self.Sock.Flags.no_block)

            # No new message exit
            if msg == self.Sock.RECV_ERROR:
                return

            # Process new Node Registration
            if isinstance(msg, self.RegistrationRequest):
                self._process_registration(msg)

            # Process Heartbeat
            elif isinstance(msg, self.HeartBeat):
                self._process_heartbeat(msg)

            # Custom Message Processing
            else:
                self.output_buffer.append(self.process_message(msg))
                # Send all msg in the buffer
                for msg in self.output_buffer:
                    self._socket_pair.send(msg)
                # Reset the output buffer
                self.output_buffer = []
