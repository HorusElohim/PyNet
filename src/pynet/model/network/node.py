# Copyright (C) 2022 HorusElohim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
from __future__ import annotations
from .. import AbcEntity, oneshot_str_hexhashing
from . import UPNP
from . import Upnp
from dataclasses import dataclass
from .patterns import *
from typing import Type
from zmq import Context
import time
import signal
import sys


class Node(AbcEntity):
    @dataclass
    class Info:
        id: int
        name: str
        start_time: int
        close_time: int
        socks: [Sock.Info]

    SERVER: Sock.SockUrl.SockType = Sock.SockUrl.SERVER
    CLIENT: Sock.SockUrl.SockType = Sock.SockUrl.CLIENT
    Sock: Type[Sock] = Sock
    Url: Sock.SockUrl = Sock.SockUrl
    UrlLocal: Sock.SockUrl.Local = Sock.SockUrl.Local
    UrlRemote: Sock.SockUrl.Remote = Sock.SockUrl.Remote
    Publisher: Type[Publisher] = Publisher
    Subscriber: Type[Subscriber] = Subscriber
    Pusher: Type[Pusher] = Pusher
    Puller: Type[Puller] = Puller
    Requester: Type[Requester] = Requester
    Replier: Type[Replier] = Replier
    Pair: Type[Pair] = Pair
    Upnp: Type[Upnp] = Upnp
    Nodes: Type[{int: Node.Info}]

    def _sigint_(self, sig: int, frame: object) -> None:
        self.log.info("CTRL-C Pressed. Cleaning resources.")
        self.log.info(f'{type(sig)}, {type(frame)}')
        self.clean_resources()
        self.log.info("Resources cleaned. Exiting ...")
        sys.exit(0)

    def __init__(self, node_name: str, enable_signal=False, **kwargs) -> None:
        AbcEntity.__init__(self, entity_name=node_name, **kwargs)
        self.node_name = f'{node_name}.Node'
        self.start_time: int = time.time_ns()
        self.close_time: int = -1
        self._socks: [Sock] = []
        if enable_signal:
            signal.signal(signal.SIGINT, self._sigint_)

    def new_publisher(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Publisher:
        self.log.debug(f'new publisher on channel: {sock_urls}')
        self._socks.append(Publisher(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_subscriber(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Subscriber:
        self.log.debug(f'new subscriber on sock_urls: {sock_urls}')
        self._socks.append(Subscriber(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_requester(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Requester:
        self.log.debug(f'new requester on sock_urls: {sock_urls}')
        self._socks.append(Requester(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_replier(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Replier:
        self.log.debug(f'new replier on sock_urls: {sock_urls}')
        self._socks.append(Replier(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_pusher(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Pusher:
        self.log.debug(f'new pusher on sock_urls: {sock_urls}')
        self._socks.append(Pusher(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_puller(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Puller:
        self.log.debug(f'new puller on sock_urls: {sock_urls}')
        self._socks.append(Puller(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_pair(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Pair:
        self.log.debug(f'new pair on url: {sock_urls}')
        self._socks.append(Pair(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_heartbeat_requester(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> HeartbeatRequester:
        self.log.debug(f'new heartbeat requester on url: {sock_urls}')
        self._socks.append(HeartbeatRequester(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    def new_heartbeat_replier(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> HeartbeatReplier:
        self.log.debug(f'new heartbeat replier on url: {sock_urls}')
        self._socks.append(HeartbeatReplier(self.node_name, sock_urls, flags=flags, logger_other=self))
        return self._socks[-1]

    @property
    def info(self) -> Info:
        return self.Info(id=oneshot_str_hexhashing(self.node_name + str(self.start_time)),
                         name=self.node_name,
                         start_time=self.start_time,
                         close_time=self.close_time,
                         socks=[s.info for s in self._socks])

    @staticmethod
    def get_upnp():
        return UPNP

    def clean_resources(self) -> None:
        pass

    def terminate(self) -> None:
        Context.instance().term()
        self.log.debug('done* ')

    def __repr__(self):
        return f'Node({str(self.info)})'

    @staticmethod
    def stamp_ns():
        return time_ns()
