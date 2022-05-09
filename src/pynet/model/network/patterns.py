from typing import Any, List, Union
from .connection import Connection
from .transmission import Transmission
from .url import Url
from .. import Logger

PATTERN_LOG = Logger('Pattern')
PATTERN_LOG.log.debug('Module Init')


class PatternBase(Connection):
    def __init__(self, name: str, connection_type: Connection.Type, pattern_type: Connection.Pattern,
                 urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=pattern_type)
        if urls:
            PATTERN_LOG.log.debug(f'{self} input urls: {urls}')
            self.url = urls
            if auto_open:
                PATTERN_LOG.log.debug(f'{self} auto open ')
                self.open()
        PATTERN_LOG.log.debug(f'{self} done *')


class Publisher(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        PatternBase.__init__(self, name, connection_type, Connection.PUB, urls, auto_open)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)


class Subscriber(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        PatternBase.__init__(self, name, connection_type, Connection.SUB, urls, auto_open)

    def receive(self) -> Any:
        return Transmission.recv(self)


class Pusher(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        PatternBase.__init__(self, name, connection_type, Connection.PUSH, urls, auto_open)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)


class Puller(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        PatternBase.__init__(self, name, connection_type, Connection.PUB, urls, auto_open)

    def receive(self) -> Any:
        return Transmission.recv(self)


class Requester(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        PatternBase.__init__(self, name, connection_type, Connection.REQ, urls, auto_open)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)

    def receive(self) -> Any:
        return Transmission.recv(self)


class Replier(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        PatternBase.__init__(self, name, connection_type, Connection.REP, urls, auto_open)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)

    def receive(self) -> Any:
        return Transmission.recv(self)


class Pair(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True):
        PatternBase.__init__(self, name, connection_type, Connection.PAIR, urls, auto_open)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)

    def receive(self) -> Any:
        return Transmission.recv(self)
