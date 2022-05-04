from zmq import Context
from typing import Any
from ..core import CoreType
from ..connection import Connection
from ..transmission import Transmission
from ..url import BaseUrl


class BaseChannel:
    def __init__(self, name: str, core_type: CoreType, context: Context):
        self.name = name
        self.core_type = core_type
        self.connections = []
        self.context = context

    def add(self, url: BaseUrl):
        self.connections.append(Connection(name=f'{self.name}_{len(self.connections)}', url=url,
                                           core_type=self.core_type, context=self.context))

    def send(self, data: Any):
        for con in self.connections:
            Transmission.send(data)