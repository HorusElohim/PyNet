import abc
from typing import Any, List, Union, Tuple
from .connection import Connection
from .transmission import Transmission
from .url import Url
from .. import Logger

PATTERN_LOG = Logger('Pattern')
PATTERN_LOG.log.debug('Module Init')


class ConnectionPatternUnsupportedOperation(Exception):
    pass


class PatternBase(Connection):
    def __init__(self, name: str, connection_type: Connection.Type, pattern_type: Connection.Pattern,
                 urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True, flags: Union[List[Tuple[int, int]], None] = None):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=pattern_type, flags=flags)
        if urls:
            PATTERN_LOG.log.debug(f'{self} input urls: {urls}')
            self.url = urls
            if auto_open:
                PATTERN_LOG.log.debug(f'{self} auto open ')
                self.open()
        PATTERN_LOG.log.debug(f'{self} done *')

    def send(self, data: Any, compression: bool = False):
        PATTERN_LOG.log.debug(f'{self} send')
        return Transmission.send(self, data, compression=compression)

    def receive(self, wait=True) -> Any:
        PATTERN_LOG.log.debug(f'{self} receive')
        return Transmission.recv(self, wait)


class Publisher(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None):
        PatternBase.__init__(self, name, connection_type, Connection.PUB, urls, auto_open, flags)
        PATTERN_LOG.log.debug(f'{self} done *')

    def receive(self) -> Any:
        PATTERN_LOG.log.error(f'{self} receive')
        raise ConnectionPatternUnsupportedOperation


class Subscriber(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None):
        PatternBase.__init__(self, name, connection_type, Connection.SUB, urls, auto_open, flags)
        PATTERN_LOG.log.debug(f'{self} done *')

    def send(self, data: Any, compression: bool = False):
        PATTERN_LOG.log.error(f'{self} send')
        raise ConnectionPatternUnsupportedOperation


class Pusher(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None):
        PatternBase.__init__(self, name, connection_type, Connection.PUSH, urls, auto_open, flags)
        PATTERN_LOG.log.debug(f'{self} done *')

    def receive(self) -> Any:
        PATTERN_LOG.log.error(f'{self} receive')
        raise ConnectionPatternUnsupportedOperation


class Puller(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None):
        PatternBase.__init__(self, name, connection_type, Connection.PULL, urls, auto_open, flags)
        PATTERN_LOG.log.debug(f'{self} done *')

    def send(self, data: Any, compression: bool = False):
        PATTERN_LOG.log.error(f'{self} send')
        raise ConnectionPatternUnsupportedOperation


class Requester(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None):
        PatternBase.__init__(self, name, connection_type, Connection.REQ, urls, auto_open, flags)
        PATTERN_LOG.log.debug(f'{self} done *')


class Replier(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None):
        PatternBase.__init__(self, name, connection_type, Connection.REP, urls, auto_open, flags)
        PATTERN_LOG.log.debug(f'{self} done *')


class Pair(PatternBase):
    def __init__(self, name: str, connection_type: Connection.Type, urls: Union[Url.BaseUrl, List[Url.BaseUrl], None] = None, auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None):
        PatternBase.__init__(self, name, connection_type, Connection.PAIR, urls, auto_open, flags)
        PATTERN_LOG.log.debug(f'{self} done *')
