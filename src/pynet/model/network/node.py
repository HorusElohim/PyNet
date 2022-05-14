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
#
from .patterns import *
from typing import Type
from zmq import Context
import time
import signal
import sys


class Node(Logger):
    Publisher: Type[Publisher] = Publisher
    Subscriber: Type[Subscriber] = Subscriber
    Pusher: Type[Pusher] = Pusher
    Puller: Type[Puller] = Puller
    Requester: Type[Requester] = Requester
    Replier: Type[Replier] = Replier
    Pair: Type[Pair] = Pair

    def _sigint_(self, sig: int, frame: object) -> None:
        self.log.info("CTRL-C Pressed. Cleaning resources.")
        self.log.info(f'{type(sig)}, {type(frame)}')
        self.clean_resources()
        self.log.info("Resources cleaned. Exiting ...")
        sys.exit(0)

    def __init__(self, name: str, enable_signal=False) -> None:
        Logger.__init__(self)
        self.name = name
        self.start_time: int = time.time_ns()
        self.close_time: int = -1
        if enable_signal:
            signal.signal(signal.SIGINT, self._sigint_)

    def new_publisher(self, url: Url.BaseUrl, connection_type: Connection.Type = Connection.SERVER) -> Publisher:
        self.log.debug(f'new publisher on channel: {url}')
        return Publisher(self.name, connection_type, url)

    def new_subscriber(self, url: Url.BaseUrl, connection_type: Connection.Type = Connection.CLIENT) -> Subscriber:
        self.log.debug(f'new subscriber on url: {url}')
        return Subscriber(self.name, connection_type, url)

    def new_requester(self, url: Url.BaseUrl, connection_type: Connection.Type = Connection.CLIENT) -> Requester:
        self.log.debug(f'new requester on url: {url}')
        return Requester(self.name, connection_type, url)

    def new_replier(self, url: Url.BaseUrl, connection_type: Connection.Type = Connection.SERVER) -> Replier:
        self.log.debug(f'new replier on url: {url}')
        return Replier(self.name, connection_type, url)

    def new_pair(self, url: Url.BaseUrl, connection_type: Connection.Type = Connection.SERVER) -> Pair:
        self.log.debug(f'new pair on url: {url}')
        return Pair(self.name, connection_type, url)

    def clean_resources(self):
        pass

    def terminate(self):
        Context.instance().term()
        self.log.debug('done* ')