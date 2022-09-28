from __future__ import annotations
from typing import Callable, Any, Dict
from time import time_ns, sleep

from ... import Cache
from .. import Node, UPNP
from . import Nodes, NodeInfo


class SteadyNodeBase(Node):
    __slots__ = 'nodes', '_socket_pair', 'cache', '_callbacks', 'active', 'spin_interval'

    def __init__(self, name: str, url: Node.Url.Remote, spin_interval=1, *args, **kwarg):
        super().__init__(name, *args, **kwarg)
        self._socket_pair = self.new_pair(url)
        self.url = url
        self.cache = Cache(self.node_name)
        self.nodes: Nodes = dict()
        self._callbacks: {type: Callable} = {}
        self.active = False
        self.spin_interval = spin_interval
        self.node_info = NodeInfo(name=self.node_name, pub_ip=UPNP.pub_ip, local_ip=UPNP.local_ip, url=self.url)

    def send(self, msg):
        self._socket_pair.send(msg)

    def recv(self, no_block=True):
        flag = 0
        if no_block:
            flag = self.Sock.Flags.no_block
        return self._socket_pair.receive(flag=flag)

    def register_callback(self, msg_type: Any, func: Callable):
        self.log.debug(f'registering callback: {{ {msg_type} : {func.__name__} }}')
        self._callbacks[msg_type] = func

    def process_callbacks(self, msg):
        # No new message exit
        if msg == self.Sock.RECV_ERROR:
            return
        # Handle new message calling the processing clb
        if type(msg) in self._callbacks:
            self.log.info(f'handled msg type : {type(msg)}')
            self._callbacks[type(msg)](msg)
        else:
            self.log.warning(f'unknown msg type : {msg}')

    def spin(self, no_block=True):
        self.active = True
        while self.active:
            self.spin_once(no_block)
            sleep(self.spin_interval)

    def spin_once(self, no_block=True):
        self.process_callbacks(self.recv(no_block))
