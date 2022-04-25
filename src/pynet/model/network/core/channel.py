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


from pathlib import Path
from typing import Union
from enum import Enum
from dataclassy import dataclass

DEFAULT_LOCAL_IP = '127.0.0.1'
DEFAULT_LOCAL_PORT = 28128
DEFAULT_LOCAL_SOCKET = '/tmp/pynet_0'


@dataclass(unsafe_hash=True, slots=True)
class BaseChannel:
    """
        BaseChannel class is the Ancestor for the Local and Remote Channel
    """
    target: str

    def __init__(self, target: str) -> None:
        """

        :param target: zmq channel

        """
        self.target = target

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}, {self.target}>'

    def __call__(self) -> str:
        """
        Simplification to return the zmq channel

        :return: zmq target channel

        """
        return self.target


class LocalChannelType(Enum):
    """
        Local Channel Type
    """
    ipc = 0
    inproc = 1


class LocalChannel(BaseChannel):
    """
        Local Channel
    """
    path: Path
    local_type: LocalChannelType

    def __init__(self, path: Union[str, Path] = DEFAULT_LOCAL_SOCKET,
                 local_type: LocalChannelType = LocalChannelType.inproc):
        """

        :param path: target path to the soocket object
        :param local_type: LocalChannelType {inproc, ipc}

        """
        self.path = Path(path)
        self.local_type = local_type
        super(LocalChannel, self).__init__(target=f'{self.local_type.name}://{self.path}')


class RemoteChannel(BaseChannel):
    """
        Remote Channel
    """
    ip: str
    port: int

    def __init__(self, ip: str = DEFAULT_LOCAL_IP, port: int = DEFAULT_LOCAL_PORT):
        """

        :param ip: target ip
        :param port: target port

        """
        self.ip = ip
        self.port = port
        super(RemoteChannel, self).__init__(target=f'tcp://{str(self.ip)}:{self.port}')
