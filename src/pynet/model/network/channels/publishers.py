from ..core import CoreType
from .base import BaseChannel, BaseUrl
from zmq import Context
from typing import List, Any
from ... import Logger

PUB_LOG = Logger('Publisher')


class Publishers(BaseChannel):
    def __init__(self, name: str, context: Context = Context.instance()):
        BaseChannel.__init__(self, name, core_type=CoreType.publisher, context=context)
        PUB_LOG.log.debug('done')        

    def publish(self, data: Any, compression=False) -> List[bool]:
        PUB_LOG.log.debug(f'sending to {self}')
        return self._send(data, compression)
