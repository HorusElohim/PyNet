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
from .. import AbcEntity
from . import UPNP
from . import Upnp
from .patterns import *
from typing import Type
from zmq import Context
import time
import signal
import sys


class Node(AbcEntity):
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
        if enable_signal:
            signal.signal(signal.SIGINT, self._sigint_)

    def new_publisher(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Publisher:
        self.log.debug(f'new publisher on channel: {sock_urls}')
        return Publisher(self.node_name, sock_urls, flags=flags, logger_other=self)

    def new_subscriber(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Subscriber:
        self.log.debug(f'new subscriber on sock_urls: {sock_urls}')
        return Subscriber(self.node_name, sock_urls, flags=flags, logger_other=self)

    def new_requester(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Requester:
        self.log.debug(f'new requester on sock_urls: {sock_urls}')
        return Requester(self.node_name, sock_urls, flags=flags, logger_other=self)

    def new_replier(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Replier:
        self.log.debug(f'new replier on sock_urls: {sock_urls}')
        return Replier(self.node_name, sock_urls, flags=flags, logger_other=self)

    def new_pusher(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Pusher:
        self.log.debug(f'new pusher on sock_urls: {sock_urls}')
        return Pusher(self.node_name, sock_urls, flags=flags, logger_other=self)

    def new_puller(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Puller:
        self.log.debug(f'new puller on sock_urls: {sock_urls}')
        return Puller(self.node_name, sock_urls, flags=flags, logger_other=self)

    def new_pair(self, sock_urls: Union[List[Url.Abc], Url.Abc], flags: Union[List[Tuple[int, int]], None] = None) -> Pair:
        self.log.debug(f'new pair on url: {sock_urls}')
        return Pair(self.node_name, sock_urls, flags=flags, logger_other=self)

    @staticmethod
    def get_upnp():
        return UPNP

    def clean_resources(self) -> None:
        pass

    def terminate(self) -> None:
        Context.instance().term()
        self.log.debug('done* ')
