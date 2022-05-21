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
    SUBSCRIBE, LINGER, NOBLOCK, EAGAIN
)
from enum import Enum
import traceback
from ... import Logger, Size, AbcEntity
from ..url import BaseUrl, Url
from typing import Union, List, Tuple

CONN_LOG = Logger('Connection')
CONN_LOG.log.debug('Module Init')

RECV_ERROR = bytes(str('ERROR').encode())


class ConnectionType(Enum):
    Server = 0,
    Client = 1


class PatternType(Enum):
    """
    Type of Connection
    """
    subscriber = SUB
    publisher = PUB
    replier = REP
    requester = REQ
    pusher = PUSH
    puller = PULL
    pair = PAIR


CONNECTION_DEFAULT_FLAGS = [
    (LINGER, 1),
]


class ConnectionUrlNotSet(Exception):
    pass


class ConnectionServerCannotHasMoreThenOneUrl(Exception):
    pass


class ConnectionBase(AbcEntity):
    """
        Connection Class
        Used to manage the zmq socket

    """

    def __init__(self, name: str, connection_type: ConnectionType, pattern_type: PatternType, flags: Union[List[Tuple[int, int]], None] = None):
        """

        :param pattern_type: Connection ZMQ Pattern Type

        """
        self._connection_name = name
        self._connection_type = connection_type
        self._connection_pattern_type = pattern_type
        self._connection_urls = []
        self._connection_flags = flags if flags else CONNECTION_DEFAULT_FLAGS
        self.is_open = False
        # ZMQ Socket
        self._socket = Context.instance().socket(self._connection_pattern_type.value)  # type: ignore[no-untyped-call]
        CONN_LOG.log.debug(f'{self} init')

    @abc.abstractmethod
    def open(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @property
    def url(self):
        if len(self._connection_urls) == 0:
            raise ConnectionUrlNotSet

        if self._connection_type == ConnectionType.Server and len(self._connection_urls) > 1:
            raise ConnectionServerCannotHasMoreThenOneUrl

        return self._connection_urls

    @url.setter
    def url(self, url: Union[BaseUrl, List[BaseUrl]]):
        if isinstance(url, BaseUrl):
            self._connection_urls.append(url)
        elif isinstance(url, list):
            self._connection_urls += url
        CONN_LOG.log.debug(f'{self} url updated')

    def __repr__(self) -> str:
        return f'<{self._connection_name}:{self._connection_type.name}:{self._connection_pattern_type.name}>'

    def _send(self, obj: bytes) -> bool:
        if not self.is_open:
            CONN_LOG.log.warning(f'{self} socket is not open')
            return False
        try:
            self._socket.send(obj)
            CONN_LOG.log.debug(f"{self} sent data with size {Size.pretty_obj_size(obj)}")
            return True
        except ZMQError as ex:
            if ex.errno == EAGAIN:
                CONN_LOG.log.warning(f"{self} resource not available. Error -> {ex}")
            else:
                CONN_LOG.log.error(f"{self} failed. Error -> {ex} \n{traceback.format_exc()}")
            return False

    def _recv(self, wait=True) -> bytes:
        if not self.is_open:
            CONN_LOG.log.warning(f'{self} socket is not open')
            return RECV_ERROR
        try:
            # Receive from the socket
            CONN_LOG.log.debug(f"{self} waiting...")
            if wait:
                obj = self._socket.recv()
            else:
                obj = self._socket.recv(NOBLOCK)
            CONN_LOG.log.debug(f"{self} received data bytes, with size {Size.pretty_obj_size(obj)}")
            return bytes(obj)
        except ZMQError as ex:
            if ex.errno == EAGAIN:
                CONN_LOG.log.warning(f"{self} resource not available. Error -> {ex}")
            else:
                CONN_LOG.log.error(f"{self} failed. Error -> {ex} \n{traceback.format_exc()}")
            return RECV_ERROR

