from .abc import AbcSock
import traceback


class SockClient(AbcSock):

    def open(self) -> bool:
        current_url = None
        if self.is_open:
            self.log.warning(f'{self} is already opened')
            return self.is_open
        try:
            for url in self.sock_urls:
                current_url = url
                self.log.debug(f'{self} connecting -> {current_url()}')
                self._socket.connect(current_url())
                for flags in self._sock_flags:
                    self.log.debug(f'{self} setting Socks flag: {flags}')
                    assert len(flags) == 2, f"{self} wrong Socks Flags {flags}"
                    self._socket.setsockopt(flags[0], flags[1])
            if self._sock_pattern_type.name == self.Pattern.subscriber.name:
                self._socket.setsockopt(self.Flags.subscribe, b'')
                self.log.debug(f'{self} subscribe set-sockopt')
            self.is_open = True
        except self.Errors and TypeError as ex:
            self.log.error(f"{self} Error opening socket for url {current_url}:\nException -> {ex}  \n{traceback.format_exc()}")
            self.is_open = False
        finally:
            self.log.debug(f'{self} socket open: {self.is_open}')
            self.log.debug(f'{self} done *')
            return self.is_open

    def close(self):
        if not self.is_open:
            self.log.warning(f'{self} the connection is not opened')
            return
        for url in self.sock_urls:
            self._socket.disconnect(url())
            self.log.debug(f'{self} disconnected from {url()}')
        self.is_open = False
        self.log.debug(f'{self} done *')
