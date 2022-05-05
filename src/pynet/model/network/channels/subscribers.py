from ..core import CoreType
from .base import BaseChannel, BaseUrl
from zmq import Context
from typing import List, Any
from ... import Logger

PUB_LOG = Logger('Subscribers')


class Subscribers(BaseChannel):
    def __init__(self, name: str, context: Context = Context.instance()):
        BaseChannel.__init__(self, name, core_type=CoreType.subscriber, context=context)

    def receive(self) -> List[Any]:
        PUB_LOG.log.debug(f'receiving from {self}')
        return self._recv()
