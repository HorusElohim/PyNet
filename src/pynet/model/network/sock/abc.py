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
    SUBSCRIBE, LINGER, DONTWAIT, NULL, RCVTIMEO,
    EAGAIN, NOBLOCK,
    ENOTSUP, ENOTSUP, EFSM, ETERM, ENOTSOCK, EFAULT
)  # https://pyzmq.readthedocs.io/en/latest/api/zmq.html
from time import time_ns
from enum import IntEnum
from ... import Size, AbcEntity, DDict
from . import SockUrl
from typing import Union, List, Tuple, Type
import logging


class SockPatternType(IntEnum):
    """
    Type of Sock
    """
    subscriber = SUB
    publisher = PUB
    replier = REP
    requester = REQ
    pusher = PUSH
    puller = PULL
    pair = PAIR


class SockFlags(IntEnum):
    null = NULL
    linger = LINGER
    dont_wait = DONTWAIT
    subscribe = SUBSCRIBE
    rcv_timeout = RCVTIMEO

    no_block = NOBLOCK


class SockError(IntEnum):
    no_data = EAGAIN
    operation_not_supported = ENOTSUP
    state_error = EFSM
    context_term = ETERM
    invalid_msg = EFAULT


SOCK_DEFAULT_FLAGS = [
    (LINGER, 1),
]


class SockUrlNotSetError(Exception):
    def __init__(self, log: logging.Logger, socks_urls: List[SockUrl.Abc]):
        log.error(f'SockUrlNotSetError -> {socks_urls} ')


class SockServerCannotHasMoreThenOneUrlError(Exception):
    def __init__(self, log: logging.Logger, socks_urls: List[SockUrl.Abc]):
        log.error(f'SockServerCannotHasMoreThenOneUrlError -> {socks_urls}')


class SockCannotBeClientAndServerError(Exception):
    def __init__(self, log: logging.Logger, socks_urls: List[SockUrl.Abc]):
        log.error(f'SockCannotBeClientAndServerError -> {socks_urls}')


class AbcSock(AbcEntity):
    SockUrl: Type[SockUrl] = SockUrl
    Pattern: Type[SockPatternType] = SockPatternType
    Flags: Type[SockFlags] = SockFlags
    Errors: Type[SockError] = SockError
    RECV_ERROR = bytes(str('ERROR').encode())

    """
        Sock Class
        Used to manage the zmq socket

    """

    def __init__(self, name: str, pattern_type: SockPatternType, flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        """

        :param name: Sock Arbitrary name
        :param pattern_type: Sock ZMQ Pattern Type
        :param flags: ZQM Flags
        :param **kwargs arguments forwarding for base class argument

        """
        AbcEntity.__init__(self, name, **kwargs)
        self._sock_name = f'{self.entity_name}.Sock'
        self._sock_pattern_type = pattern_type
        self._sock_urls: List[SockUrl.Abc] = []
        self._sock_flags = flags if flags else SOCK_DEFAULT_FLAGS
        self._sock_bytes_sent = 0
        self._sock_bytes_recv = 0
        self.is_open = False
        # ZMQ Socket
        self._socket = Context.instance().socket(self._sock_pattern_type.value)  # type: ignore[no-untyped-call]
        self.log.debug(f'{self} init')

    @property
    def info(self) -> DDict:
        return DDict(
            name=self._sock_name,
            type=self._sock_pattern_type.name,
            urls=self._sock_urls,
            flags=self._sock_flags,
            bytes_sent=self._sock_bytes_sent,
            bytes_recv=self._sock_bytes_recv,
            is_open=self.is_open,
            stamp=time_ns()
        )

    @abc.abstractmethod
    def open(self) -> bool:
        """
        open abstract method
        """
        pass

    @abc.abstractmethod
    def close(self):
        """
        close abstract method
        """
        pass

    @property
    def byte_sent(self) -> int:
        """
        byte_sent property
        """
        return self._sock_bytes_sent

    @property
    def byte_recv(self) -> int:
        """
        byte_recv property
        """
        return self._sock_bytes_recv

    @property
    def sock_urls(self) -> List[SockUrl.Abc]:
        """
        sock_urls property.getter
        """
        if len(self._sock_urls) == 0:
            raise SockUrlNotSetError(self.log, self._sock_urls)
        return self._sock_urls

    @sock_urls.setter
    def sock_urls(self, url: Union[SockUrl.Abc, List[SockUrl.Abc]]):
        """
        sock_urls property.setter
        """
        if isinstance(url, SockUrl.Abc):
            self._sock_urls.append(url)
        elif isinstance(url, list):
            self._sock_urls += url

        if self.__has_multiple_server_sock_type():
            raise SockServerCannotHasMoreThenOneUrlError(self.log, self._sock_urls)
        self.log.debug(f'{self} url updated')

    def __has_multiple_server_sock_type(self) -> bool:
        count = 0
        for url in self._sock_urls:
            if url.sock_type == self.SockUrl.SERVER:
                count += 1
        return count > 1

    def __has_different_sock_type(self) -> bool:
        server = client = False
        for url in self._sock_urls:
            if url.sock_type == self.SockUrl.SERVER:
                server = True
            elif url.sock_type == self.SockUrl.CLIENT:
                client = True
        return server is True and client is True

    @property
    def sock_type(self) -> SockUrl.SockType:
        """
        sock_type property.getter
        """
        if self.__has_different_sock_type():
            raise SockCannotBeClientAndServerError(self.log, self._sock_urls)
        return self.sock_urls[0].sock_type

    def __error_checking(self, err: ZMQError):
        error = SockError(err.errno)
        if error == SockError.no_data:
            self.log.debug(f"{self}: {error.name}")
        else:
            self.log.error(f"{self}: {error.name}")
        return self.RECV_ERROR

    def _send(self, obj: bytes, flag: int = 0) -> bool:
        if not self.is_open:
            self.log.warning(f'{self} socket is not open')
            return False
        try:
            self._socket.send(obj, flag)
            obj_size = Size.obj_size(obj)
            self._sock_bytes_sent += obj_size
            self.log.debug(f"{self} sent data with size {Size.pretty_size(obj_size)}")
            return True
        except ZMQError as ex:
            self.__error_checking(ex)
            return False

    def _recv(self, flag: int = 0) -> bytes:
        if not self.is_open:
            self.log.warning(f'{self} socket is not open')
            return self.RECV_ERROR
        try:
            # Receive from the socket
            self.log.debug(f"{self} waiting...")
            obj = self._socket.recv(flag)
            obj_size = Size.obj_size(obj)
            self._sock_bytes_recv += obj_size
            self.log.debug(f"{self} received data bytes, with size {Size.pretty_size(obj_size)}")
            return bytes(obj)
        except ZMQError as ex:
            return self.__error_checking(ex)

    def __repr__(self) -> str:
        return f'Sock({str(self.info)})'
