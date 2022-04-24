from zmq import Context
from typing import List, Any, Union
from ...common import Logger
from ..core import Connection, BaseChannel


class BasePattern(Logger):
    __name: str
    __connection_type: Connection.Type
    __connections: List[Connection]

    def __init__(self, name: str, connection_type: Connection.Type):
        super().__init__()
        self.__name = name
        self.__connection_type = connection_type
        self.__connections = []
        self.log.debug('Constructed')

    def add(self, channel: BaseChannel, context: Context):
        prev_len = len(self.__connections)
        self.__connections.append(Connection(self.__name, self.__connection_type, channel, context))
        after_len = len(self.__connections)
        if prev_len + 1 == after_len:
            self.log.debug(f'{self.__name}::success')
        else:
            self.log.error(f'{self.__name}::failed')

    def send(self, data: Any) -> bool:
        res = True
        for conn in self.__connections:
            res &= conn.send(conn, data)
        if res:
            self.log.debug(f'{self.__name}::success')
        else:
            self.log.error(f'{self.__name}::failed')
        return res

    def receive(self) -> Union[Any, List[Any]]:
        received = []
        for conn in self.__connections:
            received.append(conn.receive())
        self.log.debug(f'{self.__name}::completed')
        return received


class MethodNotSupported(Exception):
    def __init__(self, base: BasePattern, method_name: str):
        base.log.error(f"Method {method_name} not supported by {base.__class__.__name__}")
