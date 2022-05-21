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

from __future__ import annotations

import abc

from zmq import (
    Context, ZMQError,
    SUB, PUB, REQ, REP, PUSH, PULL, PAIR,
    SUBSCRIBE, LINGER, DONTWAIT, EAGAIN, NULL
)
from enum import IntEnum
import traceback
from ... import Size, AbcEntity
from . import SockUrl
from typing import Union, List, Tuple, Type

RECV_ERROR = bytes(str('ERROR').encode())


class SockPatternType(IntEnum):
    """
    Type of Sock
    """
    subscriber = SUB
    publisher = PUB
    replier = REP
    requester = REQ
    pusher = PUSH
    puller = PULL
    pair = PAIR


class SockFlags(IntEnum):
    null = NULL
    linger = LINGER
    dont_wait = DONTWAIT
    eagain = EAGAIN
    subscribe = SUBSCRIBE


SOCK_DEFAULT_FLAGS = [
    (LINGER, 1),
]


class SockUrlNotSet(Exception):
    pass


class SockServerCannotHasMoreThenOneUrl(Exception):
    pass


class SockCannotBeClientAndServer(Exception):
    pass


class AbcSock(AbcEntity):
    SockUrl: Type[SockUrl] = SockUrl
    Pattern: Type[SockPatternType] = SockPatternType
    Flags: Type[SockFlags] = SockFlags
    ERROR: Type[ZMQError] = ZMQError

    """
        Sock Class
        Used to manage the zmq socket

    """

    def __init__(self, name: str, pattern_type: SockPatternType, flags: Union[List[Tuple[int, int]], None] = None, **kwargs):
        """

        :param pattern_type: Sock ZMQ Pattern Type

        """
        AbcEntity.__init__(self, name, **kwargs)
        self._sock_name = f'{self.entity_name}.Sock'
        self._sock_pattern_type = pattern_type
        self._sock_urls: List[SockUrl.Abc] = []
        self._sock_flags = flags if flags else SOCK_DEFAULT_FLAGS
        self.is_open = False
        # ZMQ Socket
        self._socket = Context.instance().socket(self._sock_pattern_type.value)  # type: ignore[no-untyped-call]
        self.log.debug(f'{self} init')

    @abc.abstractmethod
    def open(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @property
    def sock_urls(self):
        if len(self._sock_urls) == 0:
            raise SockUrlNotSet
        return self._sock_urls

    @sock_urls.setter
    def sock_urls(self, url: Union[SockUrl.Abc, List[SockUrl.Abc]]):
        if isinstance(url, SockUrl.Abc):
            self._sock_urls.append(url)
        elif isinstance(url, list):
            self._sock_urls += url

        if self.__has_multiple_server_sock_type():
            raise SockServerCannotHasMoreThenOneUrl
        self.log.debug(f'{self} url updated')

    def __has_multiple_server_sock_type(self) -> bool:
        count = 0
        for url in self._sock_urls:
            if url.sock_type == self.SockUrl.SERVER:
                count += 1
        return count > 1

    def __has_different_sock_type(self) -> bool:
        server = client = False
        for url in self._sock_urls:
            if url.sock_type == self.SockUrl.SERVER:
                server = True
            elif url.sock_type == self.SockUrl.CLIENT:
                client = True
        return server is True and client is True

    @property
    def sock_type(self) -> SockUrl.SockType:
        if self.__has_different_sock_type():
            raise SockCannotBeClientAndServer()
        return self.sock_urls[0].sock_type

    def _send(self, obj: bytes, flag: int = 0) -> bool:
        if not self.is_open:
            self.log.warning(f'{self} socket is not open')
            return False
        try:
            self._socket.send(obj, flag)
            self.log.debug(f"{self} sent data with size {Size.pretty_obj_size(obj)}")
            return True
        except ZMQError as ex:
            if ex.errno == EAGAIN:
                self.log.warning(f"{self} resource not available. Sock msg: {ex}")
            else:
                self.log.error(f"{self} failed. Error -> {ex} \n{traceback.format_exc()}")
            return False

    def _recv(self, flag: int = 0) -> bytes:
        if not self.is_open:
            self.log.warning(f'{self} socket is not open')
            return RECV_ERROR
        try:
            # Receive from the socket
            self.log.debug(f"{self} waiting...")
            obj = self._socket.recv(flag)
            self.log.debug(f"{self} received data bytes, with size {Size.pretty_obj_size(obj)}")
            return bytes(obj)
        except ZMQError as ex:
            if ex.errno == EAGAIN:
                self.log.warning(f"{self} resource not available. Error -> {ex}")
            else:
                self.log.error(f"{self} failed. Error -> {ex} \n{traceback.format_exc()}")
            return RECV_ERROR

    def __repr__(self) -> str:
        return f'{self._sock_name}:{self._sock_pattern_type.name}'
