from .client import SockClient
from .server import SockServer


class Sock(SockServer, SockClient):

    def open(self) -> bool:
        self.log.debug(f'{self} {self.sock_urls}')
        return self._call_parent_method('open')

    def close(self):
        self.log.debug(f'{self} {self.sock_urls}')
        if self.is_open:
            self._call_parent_method('close')

    def _call_parent_method(self, method: str):
        if self.sock_type == self.SockUrl.SERVER:
            return getattr(SockServer, method)(self)
        if self.sock_type == self.SockUrl.CLIENT:
            return getattr(SockClient, method)(self)
