from typing import Any
from .connection import Connection
from .transmission import Transmission


class Publisher(Connection):
    def __init__(self, name: str, connection_type: Connection.Type):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=Connection.PUB)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)


class Subscriber(Connection):
    def __init__(self, name: str, connection_type: Connection.Type):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=Connection.SUB)

    def receive(self) -> Any:
        return Transmission.recv(self)


class Pusher(Connection):
    def __init__(self, name: str, connection_type: Connection.Type):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=Connection.PUSH)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)


class Puller(Connection):
    def __init__(self, name: str, connection_type: Connection.Type):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=Connection.PULL)

    def receive(self) -> Any:
        return Transmission.recv(self)


class Requester(Connection):
    def __init__(self, name: str, connection_type: Connection.Type):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=Connection.REQ)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)

    def receive(self) -> Any:
        return Transmission.recv(self)


class Replier(Connection):
    def __init__(self, name: str, connection_type: Connection.Type):
        super(Connection, self).__init__(name, connection_type=connection_type, pattern_type=Connection.REP)

    def send(self, data: Any, compression: bool = False):
        Transmission.send(self, data, compression=compression)

    def receive(self) -> Any:
        return Transmission.recv(self)
