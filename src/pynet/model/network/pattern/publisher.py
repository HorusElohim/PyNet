from zmq import Context
from typing import List, Any, Union
from ..core import BaseChannel, Connection
from . import BasePattern, MethodNotSupported


class Publisher(BasePattern):
    def __init__(self, name: str, channel: BaseChannel, context: Context):
        super().__init__(name, Connection.Type.publisher)
        self.add(channel, context)
        self.log.debug('Constructed')

    def receive(self, conn: Connection = None) -> Union[Any, List[Any]]:
        raise MethodNotSupported(self, 'receive')
