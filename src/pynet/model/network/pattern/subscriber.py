from zmq import Context
from typing import Any
from ..core import BaseChannel, Connection
from . import BasePattern, MethodNotSupported


class Subscriber(BasePattern):
    def __init__(self, name: str, channel: BaseChannel, context: Context):
        super().__init__(name, Connection.Type.subscriber)
        self.add(channel, context)
        self.log.debug('Constructed')

    def send(self, data: Any) -> bool:
        raise MethodNotSupported(self, 'send')
