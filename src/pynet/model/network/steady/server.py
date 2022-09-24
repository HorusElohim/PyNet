from __future__ import annotations

from . import SteadyNodeBase


class SteadyServerNode(SteadyNodeBase):
    def process_message(self, in_msg) -> object:
        return "custom-processing"

    def __init__(self, name: str, port: int):
        super().__init__(name, self.Url.Remote(self.Url.SockType.Server, '*', port))


