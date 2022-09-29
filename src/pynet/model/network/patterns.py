import threading
from dataclasses import dataclass
from time import sleep, time_ns
from typing import Any, List, Union, Tuple
from .. import DDict
from .sock import Sock
from .transmission import Transmission


class SockPatternUnsupportedOperation(Exception):
    pass


class PatternBase(Sock):
    def __init__(self, name: str, pattern_type: Sock.Pattern,
                 sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
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
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
        PatternBase.__init__(self, name, Sock.Pattern.publisher, sock_urls, auto_open, flags, **kwargs)

    def receive(self, flag: int = 0) -> Any:
        self.log.error(f'{self} receive')
        raise SockPatternUnsupportedOperation


class Subscriber(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
        PatternBase.__init__(self, name, Sock.Pattern.subscriber, sock_urls, auto_open, flags, **kwargs)

    def send(self, data: Any, flag: int = 0, compression: bool = False) -> bool:
        self.log.error(f'{self} send')
        raise SockPatternUnsupportedOperation


class Pusher(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
        PatternBase.__init__(self, name, Sock.Pattern.pusher, sock_urls, auto_open, flags, **kwargs)

    def receive(self, flag: int = 0) -> Any:
        self.log.error(f'{self} receive')
        raise SockPatternUnsupportedOperation


class Puller(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
        PatternBase.__init__(self, name, Sock.Pattern.puller, sock_urls, auto_open, flags, **kwargs)

    def send(self, data: Any, flag: int = 0, compression: bool = False) -> bool:
        self.log.error(f'{self} send')
        raise SockPatternUnsupportedOperation


class Requester(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
        PatternBase.__init__(self, name, Sock.Pattern.requester, sock_urls, auto_open, flags, **kwargs)


class Replier(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
        PatternBase.__init__(self, name, Sock.Pattern.replier, sock_urls, auto_open, flags, **kwargs)


class Pair(PatternBase):
    def __init__(self, name: str, sock_urls: Union[Sock.SockUrl.Abc, List[Sock.SockUrl.Abc], None] = None,
                 auto_open: bool = True,
                 flags: Union[List[Tuple[int, int]], None] = None,
                 **kwargs: Any) -> None:
        PatternBase.__init__(self, name, Sock.Pattern.pair, sock_urls, auto_open, flags, **kwargs)


# ______ CUSTOMS ______

@dataclass()
class HeartbeatRequest:
    sock: Sock.Info


@dataclass()
class HeartbeatReply:
    pass


class HeartbeatRequester(Requester):
    def __init__(self, hertz=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate = 1 / hertz
        self.thread = threading.Thread(target=self._heartbeat_thread_request_loop)
        self.thread.daemon = True
        self.thread.start()

    def _heartbeat_thread_request_loop(self):
        while self.is_open:
            start = time_ns()
            if self.send(HeartbeatRequest(self.info)):
                if not self.receive() == self.RECV_ERROR:
                    self.connected = True
            # if Replier is not online exit
            if not self.connected:
                break
            # Ensure processing hertz
            sleep(self.rate - (time_ns() - start) * 1e-9)
        # Close connection
        self.close()

    def __del__(self):
        self.close()
        self.thread.join()


class HeartbeatReplier(Replier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socks: Replier.Socks = {}
        self.status: {int, bool} = {}
        self.thread_loop = threading.Thread(target=self._heartbeat_thread_replier_loop)
        self.thread_loop.daemon = True
        self.thread_alive = threading.Thread(target=self._heartbeat_thread_check_alive)
        self.thread_alive.daemon = True
        self._lock = threading.Lock()
        self.thread_loop.start()
        self.thread_alive.start()

    def is_connected(self, sock_id: int):
        return self.status[sock_id]

    def _heartbeat_thread_replier_loop(self):
        while self.is_open:
            hb_req = self.receive()
            if not hb_req == self.RECV_ERROR and isinstance(hb_req, HeartbeatRequest):
                self._lock.acquire()
                self.status[hb_req.sock.id] = True
                self.socks.update({hb_req.sock.id: hb_req.sock})
                self._lock.release()
                self.send(HeartbeatReply())

    def _heartbeat_thread_check_alive(self):
        while self.is_open:
            sleep(1)
            # update all connections status
            self._lock.acquire()
            for sock_id, sock_info in self.socks.items():
                # If the last update is more the 3 seconds old
                time_delta = (time_ns() - sock_info.stamp) * 1e-9
                self.log.debug(f'last heartbeat delta: {time_delta}s')
                if (time_ns() - sock_info.stamp) * 1e-9 > 2:
                    # Set status to disconnect
                    self.status[sock_id] = False
                else:
                    # Set to connected
                    self.status[sock_id] = True
            self._lock.release()

    def __del__(self):
        self.close()
