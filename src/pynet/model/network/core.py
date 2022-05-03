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
    Context, Socket, ZMQError,
    SUB, PUB, REQ, REP, PUSH, PULL,
    SUBSCRIBE
)
from enum import Enum

from .. import Logger
from .channel import BaseChannel

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


BIND_TYPES = [CoreType.publisher, CoreType.replier, CoreType.puller]
CONNECT_TYPES = [CoreType.subscriber, CoreType.requester, CoreType.pusher]


class Core:
    """
        Connection Class
        Used to manage the zmq socket

    """

    def __init__(self, name: str, core_type: CoreType, channel: BaseChannel, context: Context = Context.instance()):
        """

        :param core_type: Connection Type
        :param channel: Target Channel
        :param context: ZMQ Context

        """
        raise_input_none('name', name)
        raise_input_none('core_type', core_type)
        raise_input_none('channel', channel)

        self.name = name
        self.core_type = core_type
        self.channel = channel

        self.socket = context.socket(self.core_type.value)
        self._open = False

        CORE_LOG.log.debug(f'{self}: init')

    def open(self):
        try:
            # Bind
            if self.core_type in BIND_TYPES:
                self.socket.bind(self.channel())
                self._open = True
                CORE_LOG.log.debug(f'{self}: bind')
            # Connect
            elif self.core_type in CONNECT_TYPES:
                self.socket.connect(self.channel())
                if self.core_type is CoreType.subscriber:
                    self.socket.setsockopt(SUBSCRIBE, b'')
                self._open = True
                CORE_LOG.log.debug(f'{self}: connect')
            else:
                CORE_LOG.log.error(f'{self}: Zmq pattern not recognized {CoreType}')

        except ZMQError as ex:
            self._open = False
            CORE_LOG.log.error(f"{self}: Error init socket for class {self}:\nException -> {ex}")

        finally:
            if self._open:
                CORE_LOG.log.debug(f'{self}: ready')
            else:
                CORE_LOG.log.warning(f'{self}: not connected!')

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
        self.socket.unbind(self.channel())
        CORE_LOG.log.debug(f'{self}: unbind ')
        self.socket.close()
        CORE_LOG.log.debug(f'{self}: closed ')

    def __repr__(self):
        return f'[{self.name}/{self.core_type.name} in {self.channel}]'


CORE_LOG.log.debug('Module Loaded')
