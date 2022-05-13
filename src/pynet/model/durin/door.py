from typing import Any
from .. import Node, Url, Process
from . import Execute, URLS, TTY


# To-Do
# Handle typing 1 character at the time
# Handle Tab
# Handle CTRL-C
# Handle PASSWORD

class DurinDoor(Node):
    replier: Node.Replier
    publisher: Node.Publisher
    tty: TTY
    active: bool = False

    def __init__(self):
        Node.__init__(self, 'DurinServer', enable_signal=True)
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
        if isinstance(data, Execute):
            if data.command == 'close':
                self.active = False
                return True
            elif data.command == 'CRTL-C':
                print(f'[CX] > {data.command}')
            else:
                print(f'[-] > {data.command}')
                try:
                    self.tty.input(data.command)
                    response = True
                except Exception as ex:
                    response = False
                    self.log.error(f'Error TTY - Exception: {ex}')
        self.log.debug(f' -> {response}')
        return response

    def console_output(self, line: str):
        self.publisher.send(line)

    def clean_resources(self):
        self.replier.close()
        self.publisher.close()
        self.tty.terminate()
        print('[x] Closed')
        self.log.debug('done * ')
