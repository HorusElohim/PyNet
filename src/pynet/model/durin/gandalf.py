from . import Execute, URLS
from .. import Node
from threading import Thread
from time import sleep
import signal
from os import system


class Console(Thread):
    subscriber: Node.Subscriber
    active: bool = False

    def __init__(self, node: Node):
        Thread.__init__(self)
        self.subscriber = node.new_subscriber(URLS.client.console)

    def run(self) -> None:
        self.active = True
        while self.active:
            print(self.subscriber.receive())

    def stop(self):
        self.active = False

    def terminate(self):
        self.stop()
        self.subscriber.close()


class Gandalf(Node):
    requester: Node.Requester
    console: Console
    active: bool = False

    def __init__(self):
        Node.__init__(self, 'DurinServer', enable_signal=False)
        self.requester = self.new_requester(URLS.client.demander)
        self.console = Console(self)
        self.console.start()
        self.log.debug('done *')
        signal.signal(signal.SIGINT, self._sigint_)

    def _sigint_(self, sig: int, frame: object) -> None:
        print("CRTL-C")
        self.demand('CRTL-C')
        system('clear')

    def demand(self, cmd: str):
        print(f'[+] Command: {cmd} -> {self.requester.url}')
        self.requester.send(Execute(command=cmd))
        res = self.requester.receive()
        if res == 'Closed':
            print('Durin Door Closed')
            self.stop()
        self.log.debug(f'{self} done {res}')

    def start(self):
        print('Gandalf has started!')
        self.active = True
        while self.active:
            sleep(0.1)
            cmd = input('> ')
            self.demand(cmd)
        self.log.debug('done * ')

    def clean_resources(self):
        self.requester.close()
        self.active = False

    def stop(self):
        print("Exiting ... ")
        self.console.terminate()
        self.console.join(timeout=1)
        self.active = False
