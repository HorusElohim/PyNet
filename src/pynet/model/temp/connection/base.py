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
from typing import List
from dataclassy import dataclass
from enum import Enum

from ... import Logger
from .. import BaseChannel, Packet


class ConnectionBaseArgIsNone(Exception):
    pass


@dataclass(slots=True)
class ConnectionBase(Logger):
    """
        Connection Class
        Used to manage the zmq socket

    """

    class Type(Enum):
        """
        Type of Connection
        """
        subscriber = SUB
        publisher = PUB
        replier = REP
        requester = REQ
        pusher = PUSH
        puller = PULL

    def __init__(self, name: str, connection_type: Type, channel: BaseChannel, context: Context = Context.instance()):
        """

        :param connection_type: Connection Type
        :param channel: Target Channel
        :param context: ZMQ Context

        """
        self.__raise_input_none('name', name)
        self.__raise_input_none('type', connection_type)
        self.__raise_input_none('channel', channel)

        self.name = name
        self.type = connection_type
        self.channel = channel
        self.socket = context.socket(self.type.value)
        self.open = False
        self.__bind_types = [self.Type.publisher, self.Type.replier, self.Type.puller]
        self.__connect_types = [self.Type.subscriber, self.Type.requester, self.Type.pusher]

        try:
            if self.type in self.__bind_types:
                self.__bind()
            elif self.type in self.__connect_types:
                self.__connect()
            else:
                self.__unrecognized_connection_type()

        except ZMQError as ex:
            self.__error(ex)

        finally:
            if self.open:
                self.__ready()
            else:
                self.__not_connected()

    def __raise_input_none(self, name: str, arg: object) -> None:
        if not arg:
            self.log.error(f'Error input {name} is None')
            raise ConnectionBaseArgIsNone

    def __error(self, exception: ZMQError) -> None:
        self.open = False
        self.log.error(f"Error init socket for class {self}\nException -> {exception}")

    def __ready(self) -> None:
        self.log.debug(f'{self.name}::{self.type.name} ready on channel ->{self.channel}')

    def __not_connected(self) -> None:
        self.log.warning(f'{self.name}::{self.type.name} not connected on channel ->{self.channel}')

    def __unrecognized_connection_type(self) -> None:
        self.log.error(f'Zmq pattern not recognized {self.Type}')

    def __bind(self) -> None:
        self.socket.bind(self.channel())
        self.open = True
        self.log.debug(f'{self.name}::{self.type.name} on channel {self.channel()}')

    def __connect(self) -> None:

        self.socket.connect(self.channel())
        if self.type is self.Type.subscriber:
            self.socket.setsockopt(SUBSCRIBE, b'')
        self.open = True
        self.log.debug(f'{self.name}::{self.type.name} on channel {self.channel()}')

    def create_packet(self, data: object = None) -> Packet:
        """
        Create Packet

        :param: data: User Data
        :return: Packet

        """
        return Packet(sender=self.name, channel=self.channel(), data=data)

    def is_connection_open(self) -> bool:
        """
        Is the connection open

        :return: connection open

        """
        return self.open

    def close(self) -> None:
        """
        Close Connection
        """
        self.open = False
        self.socket.close()
        self.log.debug('Closed')
