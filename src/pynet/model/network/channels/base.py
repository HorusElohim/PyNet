from zmq import Context
from typing import Any, List, Dict
from ..core import CoreType
from ..connection import Connection
from ..transmission import Transmission
from ..url import BaseUrl
from ... import Logger

CHA_LOG = Logger('BaseChannel')


class BaseChannel:
    def __init__(self, name: str, core_type: CoreType, context: Context = Context.instance()):
        self.name = name
        self.core_type = core_type
        self.connections: Dict[str, Connection] = {}
        self.context = context
        CHA_LOG.log.debug('done')

    def add(self, name: str, url: BaseUrl):
        self.connections.update({
            name: Connection(name=f'{self.name}.{name}', url=url, core_type=self.core_type, context=self.context)
        })
        self.connections[name].open()
        CHA_LOG.log.debug('done')

    def send(self, data: Any, compression=False) -> List[bool]:
        res = []
        for name, con in self.connections.items():
            res.append(Transmission.send(con, data, compression=compression))
            CHA_LOG.log.debug(f'{name} recv completed')
        CHA_LOG.log.debug('done')
        return res

    def recv(self) -> List[Any]:
        res = []
        for name, con in self.connections.items():
            res.append(Transmission.recv(con))
            CHA_LOG.log.debug(f'{name} send completed')
        CHA_LOG.log.debug('done')
        return res

    def close(self):
        for name, con in self.connections.items():
            con.close()
            CHA_LOG.log.debug(f'{name} close completed')
        CHA_LOG.log.debug('done')
