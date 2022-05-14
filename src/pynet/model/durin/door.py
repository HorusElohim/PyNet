from typing import Any
from .. import Node, Url, Process
from . import Execute, URLS, TTY


class DurinDoor(Node):
    replier: Node.Replier
    publisher: Node.Publisher
    tty: TTY
    active: bool = False

    def __init__(self):
        Node.__init__(self, 'Durin', enable_signal=False)
        self.replier = self.new_replier(URLS.server.demander)
        self.publisher = self.new_publisher(URLS.server.console)
        self.tty = TTY(self.publisher)
        self.log.debug('done *')

    def start(self):
        print('Durin Door has started!')
        self.active = True
        self.tty.start()
        while self.active:
            self.replier.send(self.dispatch(self.replier.receive()))
        self.clean_resources()

    def dispatch(self, data: Any) -> Any:
        self.log.debug(f' <- {data}')
        response = False
        try:
            if isinstance(data, Execute):
                if data.command == 'close':
                    self.stop()
                    response = 'close'
                else:
                    print(f'> {data.command}')
                    self.tty.input(data.command)
                    response = True
        except Exception as ex:
            response = False
            self.log.error(f'Error TTY - Exception: {ex}')
        self.log.debug(f' -> {response}')
        return response

    def stop(self):
        self.active = False

    def clean_resources(self):
        self.replier.close()
        self.publisher.close()
        self.tty.terminate()
        print('[x] Closed')
        self.log.debug('done * ')
