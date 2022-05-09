from typing import Any
from .. import Node, Url, Process
from . import Exit, Execute, URL_CONSOLE_SERVER, URL_REQUEST_SERVER


class DurinDoor(Node):
    replier: Node.Replier
    active: bool = False

    def __init__(self):
        Node.__init__(self, 'DurinServer', enable_signal=True)
        self.replier = self.new_replier(URL_REQUEST_SERVER)
        self.publisher = self.new_publisher(URL_CONSOLE_SERVER)
        self.process = Process(self.console_output)
        self.active = True
        self.log.debug('done *')

    def start(self):
        self.log.debug('starting ...')
        while self.active:
            self.replier.send(self.dispatch(self.replier.receive()))
        self.log.debug('done * ')

    def dispatch(self, data: Any) -> Any:
        self.log.debug(f'{self} <- {data}')
        response = False
        if isinstance(data, Execute):
            res = self.process.run(data.command)
            response = True if res == 0 else False
        if isinstance(data, Exit):
            self.active = False
            response = True

        self.log.debug(f'{self} -> {response}')
        return response

    def console_output(self, line: str):
        self.publisher.send(line)
