from __future__ import annotations

from . import SteadyNodeBase


class SteadyClientNode(SteadyNodeBase):
    def __init__(self, name: str, ip: str, port: int):
        super().__init__(name, self.Url.Remote(self.Url.SockType.Client, ip, port))

    def process_message(self, in_msg) -> object:
        return "custom-processing"
