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

from zmq import Context
from typing import Type, Union
from ..common import Logger
from . import BaseChannel
from . import Subscriber, Publisher
import time
import signal
import sys


class Node(Logger):
    def _sigint_(self, sig: int, frame: object) -> None:
        self.log.info("CTRL-C Pressed. Cleaning resources.")
        self.log.info(f'{type(sig)}, {type(frame)}')
        self._context.destroy()
        self.log.info("Resources cleaned. Exiting ...")
        sys.exit(0)

    def __init__(self, name: str, context: Union[Context, None] = None) -> None:
        Logger.__init__(self)
        self.name = name
        self._context = context or Context.instance()
        self.start_time: int = time.time_ns()
        self.close_time: int = -1
        signal.signal(signal.SIGINT, self._sigint_)

    def publisher(self, channel: BaseChannel) -> Publisher:
        self.log.debug(f'new publisher on channel: {channel}')
        return self._Publisher(self.name, channel, self._context)

    def subscriber(self, channel: BaseChannel) -> Subscriber:
        self.log.debug(f'new subscriber on channel: {channel}')
        return self._Subscriber(self.name, channel, self._context)
