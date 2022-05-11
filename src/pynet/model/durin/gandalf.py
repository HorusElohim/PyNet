from . import Execute, URL_REQUEST_CLIENT, URL_CONSOLE_CLIENT
from .. import Node
from threading import Thread
from time import sleep
import signal


class Console(Thread):
    subscriber: Node.Subscriber
    active: bool = False

    def __init__(self, node: Node):
        Thread.__init__(self)
        self.subscriber = node.new_subscriber(URL_CONSOLE_CLIENT)

    def run(self) -> None:
        self.active = True
        while self.active:
            print(self.subscriber.receive())

    def stop(self):
        self.active = False
        self.subscriber.close()


class Gandalf(Node):
    requester: Node.Requester
    console: Console
    active: bool = False

    def __init__(self):
        Node.__init__(self, 'DurinServer', enable_signal=True)
        self.requester = self.new_requester(URL_REQUEST_CLIENT)
        self.console = Console(self)
        self.console.start()
        self.log.debug('done *')

    def _sigint_(self, sig: int, frame: object) -> None:
        pass

    def demand(self, cmd: str):
        print(f'[+] Command: {cmd} -> {self.requester.url}')
        self.requester.send(Execute(command=cmd))
        res = self.requester.receive()
        self.log.debug(f'{self} done {res}')

    def start(self):
        print('Gandalf has started!')
        self.active = True
        while self.active:
            sleep(0.3)
            cmd = input('> ')
            self.demand(cmd)
            if cmd == 'exit':
                self.active = False
                print('Exiting...')
                self.console.stop()
        self.log.debug('done * ')

    def clean_resources(self):
        self.requester.close()
