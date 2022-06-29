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
from typing import Union, TypeAlias
from enum import Enum
from dataclasses import dataclass

DEFAULT_LOCAL_IP = '127.0.0.1'
DEFAULT_LOCAL_PORT = 28128
DEFAULT_LOCAL_SOCKET = '/tmp/pynet_0'


class SockType(Enum):
    Server = 0,
    Client = 1


class AbcSocketUrlException(Exception):
    def __init__(self) -> None:
        print("AbcSockUrl cannot be used directly.\nUse instead RemoteSockUrl or LocalSockUrl !")


@dataclass(unsafe_hash=True)
class AbcSockUrl:
    __slots__ = 'sock_type'
    sock_type: SockType

    """
        BaseChannel class is the Ancestor for the Local and Remote Channel
    """

    def __init__(self, sock_type: SockType):
        self.sock_type = sock_type

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}::{self.__call__()}>'

    def __call__(self) -> str:
        """
        Simplification to return the zmq channel

        :return: zmq target channel

        """
        if isinstance(self, RemoteSockUrl):
            return f'tcp://{str(self.ip)}:{self.port}'
        elif isinstance(self, LocalSockUrl):
            return f'{self.local_type.name}://{self.path}'
        else:
            raise AbcSocketUrlException


class LocalSockType(Enum):
    """
        Local Channel Type
    """
    ipc = 0
    inproc = 1


class LocalSockUrl(AbcSockUrl):
    """
        Local Channel
    """
    __slots__ = ('path', 'local_type')
    path: Path
    local_type: LocalSockType

    def __init__(self, sock_type: SockType, path: Union[str, Path] = DEFAULT_LOCAL_SOCKET,
                 local_type: LocalSockType = LocalSockType.inproc):
        """

        :param path: target path to the soocket object
        :param local_type: LocalType {inproc, ipc}

        """
        AbcSockUrl.__init__(self, sock_type=sock_type)
        self.path = Path(path)
        self.local_type = local_type


class RemoteSockUrl(AbcSockUrl):
    """
        Remote Channel
    """
    __slots__ = ('ip', 'port')

    ip: str
    port: int

    def __init__(self, sock_type: SockType, ip: str = DEFAULT_LOCAL_IP, port: int = DEFAULT_LOCAL_PORT):
        """

        :param ip: target ip
        :param port: target port

        """
        AbcSockUrl.__init__(self, sock_type=sock_type)
        self.ip = ip
        self.port = port


class SockUrl:
    Abc: TypeAlias = AbcSockUrl
    Remote: TypeAlias = RemoteSockUrl
    Local: TypeAlias = LocalSockUrl
    LocalType: TypeAlias = LocalSockType
    SockType: TypeAlias = SockType
    INPROC: LocalType = LocalSockType.inproc
    IPC: LocalType = LocalSockType.ipc
    SERVER: SockType = SockType.Server
    CLIENT: SockType = SockType.Client
