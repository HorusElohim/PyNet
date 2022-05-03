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
from .core import Core, CoreType
from zmq import ZMQError

CONN_LOG = Logger('Connection')
CONN_LOG.log.debug('Module Init')


class Connection(Core):

    def send(self, obj: bytes):
        try:
            CONN_LOG.log.debug(f"sending data with size {Size.pretty_obj_size(obj)}")
            self.socket.send(obj)
            CONN_LOG.log.debug("success")
            return True
        except ZMQError as ex:
            CONN_LOG.log.error(f"failed. Error -> {ex}")
            return False

    def recv(self) -> bytes:
        try:
            # Receive from the socket
            CONN_LOG.log.debug(f"{self}: waiting...")
            obj = self.decode(self.socket.recv())  # type: ignore[arg-type]
            CONN_LOG.log.debug(f"{self}: received data {obj}, with size {Size.pretty_obj_size(obj)}")
            return obj
        except ZMQError as ex:
            CONN_LOG.log.error(f"{self}: Error -> {ex}")
            return bytes(str('ERROR').encode())


CONN_LOG.log.debug('Module Loaded')
