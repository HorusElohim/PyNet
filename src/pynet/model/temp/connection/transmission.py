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
from typing import Union
from zmq import ZMQError

from .. import Packet
from . import ConnectionBase


class TryToUseConnectionTransmissionOnClosedConnection(Exception):
    pass


class ConnectionTransmission(ConnectionBase):

    def safe_check(self) -> ConnectionTransmission:
        """
        Safe check before use any transmissions methods

        :return: self instance to concatenate methods

        """
        if self.open:
            return self
        else:
            raise TryToUseConnectionTransmissionOnClosedConnection

    def __receive(self) -> Union[Packet, object]:
        """
        Receive main internal method

        :return: received data

        """
        try:
            # Receive from the socket
            obj = self.decode(self.socket.recv())  # type: ignore[arg-type]
            self.log.debug(f"{obj}")
            return obj
        except ZMQError as ex:
            self.log.error(f"Error -> {ex}")
            return None

    def receive(self, raw: bool = False) -> Union[Packet, object]:
        """
        Receive method

        :param: raw: flag to receive data raw
        :return: received data

        """
        obj = self.safe_check().__receive()
        if raw:
            return obj
        else:
            if isinstance(obj, Packet):
                return self.decode_packet(obj)
            else:
                self.log.warning("Not a Packet received with raw set to False")
                return obj

    def __send(self, obj: object) -> bool:
        """
        Send main internal method

        :param: obj: target object to send
        :return: success or fail flag

        """
        try:
            self.log.debug(f"{obj}")
            self.socket.send(self.encode(obj))
            self.log.debug("success")
            return True
        except ZMQError as ex:
            self.log.error(f"failed. Error -> {ex}")
            return False

    def send(self, obj: object, as_packet: bool = True) -> bool:
        """
        Send method

        :param: obj: target object to send
        :param: as_packet: flag if needed the encapsulation in a Packet
        :return: success or fail flag

        """
        if as_packet and not isinstance(obj, Packet):
            # create packet with obj as data
            obj = self.create_packet(obj)

        return self.safe_check().__send(obj)
