from typing import Any, List, Union, Tuple
from .sock import Sock
from .transmission import Transmission


class SockPatternUnsupportedOperation(Exception):
    pass


class PatternBase(Sock):
    def __init__(self, name: str, pattern_type: Sock.Pattern,
                 sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        super(Sock, self).__init__(name, pattern_type=pattern_type, flags=flags, **kwargs)
        if sock_urls:
            self.log.debug(f'{self} input sock_urls: {sock_urls}')
            self.sock_urls = sock_urls
            if auto_open:
                self.log.debug(f'{self} auto open ')
                self.open()

    def send(self, data: Any, flag: int = 0, compression: bool = False) -> bool:
        return Transmission.send(self, data, flag, compression=compression)

    def receive(self, flag: int = 0) -> Any:
        return Transmission.recv(self, flag)


class Publisher(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        PatternBase.__init__(self, name, Sock.Pattern.publisher, sock_urls, auto_open, flags, **kwargs)

    def receive(self, flag: int = 0) -> Any:
        self.log.error(f'{self} receive')
        raise SockPatternUnsupportedOperation


class Subscriber(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        PatternBase.__init__(self, name, Sock.Pattern.subscriber, sock_urls, auto_open, flags, **kwargs)

    def send(self, data: Any, flag: int = 0, compression: bool = False) -> bool:
        self.log.error(f'{self} send')
        raise SockPatternUnsupportedOperation


class Pusher(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        PatternBase.__init__(self, name, Sock.Pattern.pusher, sock_urls, auto_open, flags, **kwargs)

    def receive(self, flag: int = 0) -> Any:
        self.log.error(f'{self} receive')
        raise SockPatternUnsupportedOperation


class Puller(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        PatternBase.__init__(self, name, Sock.Pattern.puller, sock_urls, auto_open, flags, **kwargs)

    def send(self, data: Any, flag: int = 0, compression: bool = False) -> bool:
        self.log.error(f'{self} send')
        raise SockPatternUnsupportedOperation


class Requester(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        PatternBase.__init__(self, name, Sock.Pattern.requester, sock_urls, auto_open, flags, **kwargs)


class Replier(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        PatternBase.__init__(self, name, Sock.Pattern.replier, sock_urls, auto_open, flags, **kwargs)


class Pair(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open=True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs):
        PatternBase.__init__(self, name, Sock.Pattern.pair, sock_urls, auto_open, flags, **kwargs)
