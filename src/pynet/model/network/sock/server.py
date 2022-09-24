from .abc import AbcSock


class SockServer(AbcSock):
    def open(self) -> bool:
        if self.is_open:
            self.log.warning(f'{self} is already opened')
            return self.is_open
        try:
            # BIND
            self.log.debug(f'{self} binding -> {self.sock_urls[0]()}')
            self._socket.bind(self.sock_urls[0]())
            # Flags assignments
            for flags in self._sock_flags:
                self.log.debug(f'{self} setting Connections flag: {flags}')
                assert len(flags) == 2, f"{self} wrong Connections Flags {flags}"
                self._socket.setsockopt(flags[0], flags[1])
            # Additional subscriber flag
            if self._sock_pattern_type.name == self.Pattern.subscriber.name:
                self._socket.setsockopt(self.Flags.subscribe, b'')
                self.log.debug(f'{self} subscribe set-sockopt')
            # Now is open
            self.is_open = True
        except self.Errors as ex:
            self.log.error(f"{self} Error opening socket for sock_url {self.sock_urls}:\nException -> {ex}")
            self.is_open = False
        finally:
            self.log.debug(f'{self} socket open: {self.is_open}')
            self.log.debug(f'{self} done *')
            return self.is_open

    def _unbind(self):
        sock_urls = self._socket.LAST_ENDPOINT
        self.log.debug(f'{self} unbinding -> {sock_urls}')
        self._socket.unbind(sock_urls)
        self.log.debug(f'{self} done *')

    def close(self):
        self._unbind()
        self._socket.close()
        self.is_open = False
        self.log.debug(f'{self} done *')
