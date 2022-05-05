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

from .. import Logger, Size
from .core import Core
from zmq import ZMQError

CONN_LOG = Logger('Connection')
CONN_LOG.log.debug('Module Init')


class Connection(Core):

    def send(self, obj: bytes) -> bool:
        if not self.is_open():
            CONN_LOG.log.warning(f'{self} core is not open')
            return False
        try:
            self.socket.send(obj)
            CONN_LOG.log.debug(f"{self} sent data with size {Size.pretty_obj_size(obj)}")
            return True
        except ZMQError as ex:
            CONN_LOG.log.error(f"{self} failed. Error -> {ex}")
            return False

    def recv(self) -> bytes:
        if not self.is_open():
            CONN_LOG.log.warning(f'{self} core is not open')
            return bytes(str('ERROR').encode())
        try:
            # Receive from the socket
            CONN_LOG.log.debug(f"{self}: waiting...")
            obj = self.socket.recv()
            CONN_LOG.log.debug(f"{self}: received data bytes, with size {Size.pretty_obj_size(obj)}")
            return bytes(obj)
        except ZMQError as ex:
            CONN_LOG.log.error(f"{self}: Error -> {ex}")
            return bytes(str('ERROR').encode())


CONN_LOG.log.debug('Module Loaded')
