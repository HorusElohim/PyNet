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
    SUBSCRIBE
)
from enum import Enum

from .. import Logger, Size
from .url import BaseUrl, Url
from typing import Union, List

CONN_LOG = Logger('Connection')
CONN_LOG.log.debug('Module Init')


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


class ConnectionUrlNotSet(Exception):
    pass


class ConnectionServerCannotHasMoreThenOneUrl(Exception):
    pass


class ConnectionBase:
    """
        Connection Class
        Used to manage the zmq socket

    """

    def __init__(self, name: str, connection_type: ConnectionType, pattern_type: PatternType):
        """

        :param pattern_type: Connection ZMQ Pattern Type

        """

        self._connection_name = name
        self._connection_type = connection_type
        self._connection_pattern_type = pattern_type
        self._connection_urls = []
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
            CONN_LOG.log.warning(f'{self} core is not open')
            return False
        try:
            self._socket.send(obj)
            CONN_LOG.log.debug(f"{self} sent data with size {Size.pretty_obj_size(obj)}")
            return True
        except ZMQError as ex:
            CONN_LOG.log.error(f"{self} failed. Error -> {ex}")
            return False

    def _recv(self) -> bytes:
        if not self.is_open:
            CONN_LOG.log.warning(f'{self} core is not open')
            return bytes(str('ERROR').encode())
        try:
            # Receive from the socket
            CONN_LOG.log.debug(f"{self} waiting...")
            obj = self._socket.recv()
            CONN_LOG.log.debug(f"{self} received data bytes, with size {Size.pretty_obj_size(obj)}")
            return bytes(obj)
        except ZMQError as ex:
            CONN_LOG.log.error(f"{self} Error -> {ex}")
            return bytes(str('ERROR').encode())


class ConnectionServerBase(ConnectionBase):
    def open(self) -> bool:
        if self.is_open:
            CONN_LOG.log.warning(f'{self} is already opened')
            return self.is_open
        try:
            CONN_LOG.log.debug(f'{self} binding -> {self.url[0]()}')
            self._socket.bind(self.url[0]())
            if self._connection_pattern_type.name == PatternType.subscriber.name:
                self._socket.setsockopt(SUBSCRIBE, b'')
                CONN_LOG.log.debug(f'{self} subscribe set-sockopt')
                # res = self._socket.poll(timeout=0)
                # CONN_LOG.log.debug(f'{self} (Bug-LIBZMQ-270) polling first time: {res}')
            self.is_open = True
            CONN_LOG.log.debug(f'{self} done *')
        except ZMQError as ex:
            CONN_LOG.log.error(f"{self} Error opening socket for url {self.url}:\nException -> {ex}")
            self.is_open = False
        finally:
            return self.is_open

    def _unbind(self):
        url = self._socket.LAST_ENDPOINT
        CONN_LOG.log.debug(f'{self} unbinding -> {url}')
        self._socket.unbind(url)
        CONN_LOG.log.debug(f'{self} done *')

    def close(self):
        self._unbind()
        self._socket.close()
        self.is_open = False
        CONN_LOG.log.debug(f'{self} done *')


class ConnectionClientBase(ConnectionBase):

    def open(self) -> bool:
        if self.is_open:
            CONN_LOG.log.warning(f'{self} is already opened')
            return self.is_open
        try:
            for url in self.url:
                CONN_LOG.log.debug(f'{self} connecting -> {url()}')
                self._socket.connect(url())
            if self._connection_pattern_type.name == PatternType.subscriber.name:
                self._socket.setsockopt(SUBSCRIBE, b'')
                CONN_LOG.log.debug(f'{self} subscribe set-sockopt')
            CONN_LOG.log.debug(f'{self} done *')
            self.is_open = True
        except ZMQError as ex:
            CONN_LOG.log.error(f"{self} Error opening socket for url {self.url}:\nException -> {ex}")
            self.is_open = False
        except TypeError as terr:
            CONN_LOG.log.error(f"{self} Error opening socket for url {self.url}:\nException -> {terr}")
        finally:
            return self.is_open

    def close(self):
        if not self.is_open:
            CONN_LOG.log.warning(f'{self} the connection is not opened')
            return
        for url in self.url:
            self._socket.disconnect(url())
            CONN_LOG.log.debug(f'{self} disconnected from {url()}')
        self.is_open = False
        CONN_LOG.log.debug(f'{self} done *')


class Connection(ConnectionServerBase, ConnectionClientBase):
    Type: ConnectionType = ConnectionType
    Pattern: PatternType = PatternType
    SERVER: ConnectionType = ConnectionType.Server
    CLIENT: ConnectionType = ConnectionType.Client
    PUB: PatternType = PatternType.publisher
    SUB: PatternType = PatternType.subscriber
    PUSH: PatternType = PatternType.pusher
    PULL: PatternType = PatternType.puller
    REQ: PatternType = PatternType.requester
    REP: PatternType = PatternType.replier
    PAIR: PatternType = PatternType.pair

    def open(self) -> bool:
        CONN_LOG.log.debug(f'{self} {self.url}')
        return self._call_parent_method('open')

    def close(self):
        CONN_LOG.log.debug(f'{self} {self.url}')
        self._call_parent_method('close')

    def _call_parent_method(self, method: str):
        if self._connection_type == ConnectionType.Server:
            return getattr(ConnectionServerBase, method)(self)
        if self._connection_type == ConnectionType.Client:
            return getattr(ConnectionClientBase, method)(self)


CONN_LOG.log.debug('Module Loaded')
