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
from zmq import (
    Context, ZMQError,
    SUB, PUB, REQ, REP, PUSH, PULL,
    SUBSCRIBE
)
from enum import Enum

from .. import Logger
from .url import BaseUrl, Url

CORE_LOG = Logger('Core')
CORE_LOG.log.debug('Module Init')


class CoreArgIsNone(Exception):
    pass


def raise_input_none(name: str, arg: object) -> None:
    if not arg:
        CORE_LOG.log.error(f'Error input {name} is None')
        raise CoreArgIsNone


class CoreType(Enum):
    """
    Type of Connection
    """
    subscriber = SUB
    publisher = PUB
    replier = REP
    requester = REQ
    pusher = PUSH
    puller = PULL


class Core:
    """
        Connection Class
        Used to manage the zmq socket

    """

    def __init__(self, name: str, core_type: CoreType, url: BaseUrl, context: Context = Context.instance()):
        """

        :param core_type: Connection Type
        :param url: Target Channel
        :param context: ZMQ Context

        """
        raise_input_none('name', name)
        raise_input_none('core_type', core_type)
        raise_input_none('url', url)

        self.name = name
        self.core_type = core_type
        self.url = url

        self.socket = context.socket(self.core_type.value)  # type: ignore[no-untyped-call]
        self._open = False

        CORE_LOG.log.debug(f'{self}: init')

    def _bind(self):
        self.socket.bind(self.url())
        CORE_LOG.log.debug(f'{self}: ok')

    def _unbind(self):
        self.socket.unbind(self.url())
        CORE_LOG.log.debug(f'{self}: ok')

    def _connect(self):
        self.socket.connect(self.url())
        CORE_LOG.log.debug(f'{self}: ok')

    def _disconnect(self):
        self.socket.disconnect(self.url())
        CORE_LOG.log.debug(f'{self}: ok')

    def open(self) -> bool:
        if self.is_open():
            CORE_LOG.log.warning('try to open Core already opened!')
            return True

        try:
            if self.url.socket_type == Url.SocketType.bind:
                self._bind()
                self._open = True
            elif self.url.socket_type == Url.SocketType.connect:
                self._connect()
                self._open = True
            if self.core_type is CoreType.subscriber:
                CORE_LOG.log.debug(f'{self}: is type subscriber')
                self.socket.setsockopt(SUBSCRIBE, b'')
            CORE_LOG.log.debug(f'{self}: ok')
        except ZMQError as ex:
            CORE_LOG.log.error(f"{self}: Error opening socket for url {self.url}:\nException -> {ex}")
            self._open = False
        finally:
            if self._open:
                CORE_LOG.log.debug(f'{self}: ready')
            else:
                CORE_LOG.log.error(f'{self}: not connected!')
            return self._open

    def is_open(self) -> bool:
        """
        Is the connection open

        :return: connection open

        """
        return self._open

    def close(self) -> None:
        """
        Close Connection
        """
        self._open = False
        if self.url.socket_type == Url.SocketType.bind:
            self._unbind()
        elif self.url.socket_type == Url.SocketType.connect:
            self._disconnect()
        self.socket.close()
        CORE_LOG.log.debug(f'{self}: closed ')

    def __repr__(self) -> str:
        return f'[{self.name}/{self.core_type.name} in {self.url}]'


CORE_LOG.log.debug('Module Loaded')
