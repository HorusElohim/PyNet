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
from typing import Union, Type
from enum import Enum
from dataclassy import dataclass

DEFAULT_LOCAL_IP = '127.0.0.1'
DEFAULT_LOCAL_PORT = 28128
DEFAULT_LOCAL_SOCKET = '/tmp/pynet_0'


@dataclass(unsafe_hash=True, slots=True)
class BaseUrl:
    """
        BaseChannel class is the Ancestor for the Local and Remote Channel
    """

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}::{self.__call__()}>'

    def __call__(self) -> str:
        """
        Simplification to return the zmq channel

        :return: zmq target channel

        """
        if isinstance(self, RemoteUrl):
            return f'tcp://{str(self.ip)}:{self.port}'
        elif isinstance(self, LocalUrl):
            return f'{self.local_type.name}://{self.path}'


class LocalType(Enum):
    """
        Local Channel Type
    """
    ipc = 0
    inproc = 1


class LocalUrl(BaseUrl):
    """
        Local Channel
    """
    path: Path
    local_type: LocalType

    def __init__(self, path: Union[str, Path] = DEFAULT_LOCAL_SOCKET,
                 local_type: LocalType = LocalType.inproc):
        """

        :param path: target path to the soocket object
        :param local_type: LocalType {inproc, ipc}

        """
        BaseUrl.__init__(self)
        self.path = Path(path)
        self.local_type = local_type


class RemoteUrl(BaseUrl):
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
        BaseUrl.__init__(self)
        self.ip = ip
        self.port = port


class Url:
    BaseUrl: Type[BaseUrl] = BaseUrl
    Remote: Type[RemoteUrl] = RemoteUrl
    Local: Type[LocalUrl] = LocalUrl
    LocalType: Type[LocalType] = LocalType
    INPROC: LocalType = LocalType.inproc
    IPC: LocalType = LocalType.ipc
