import os
import signal

from . import Execute, URLS
from .. import Node
from typing import Any
from threading import Thread
from time import sleep


class Console(Thread):
    subscriber: Node.Subscriber
    active: bool = False
    last_recv: str

    def __init__(self, subscriber: Node.Subscriber):
        Thread.__init__(self)
        self.subscriber = subscriber
        self.last_recv = ''

    def run(self) -> None:
        self.active = True
        while self.active:
            self.last_recv = self.subscriber.receive()
            print(self.last_recv)

    def stop(self):
        self.active = False


class Gandalf(Node):
    requester: Node.Requester
    subscriber: Node.Subscriber
    console: Console
    active: bool = False

    def __init__(self):
        Node.__init__(self, 'Gandalf', enable_signal=False)
        self.requester = self.new_requester(URLS.client.demander)
        self.subscriber = self.new_subscriber(URLS.client.console)
        self.console = Console(self.subscriber)
        self.console.start()
        self.log.debug('done *')

    def demand(self, cmd: str) -> Any:
        self.requester.send(Execute(command=cmd))
        res = self.requester.receive()
        self.log.debug(f'{self} done {res}')
        return res

    def start(self):
        print('Gandalf has started!')
        self.active = True
        while self.active:
            cmd = input('')
            answer = self.demand(cmd)
            if answer == 'close':
                self.stop()
        self.clean_resources()
        print('Exiting ...')
        self.log.debug('done * ')
        os.kill(os.getpid(), signal.SIGKILL)

    def clean_resources(self):
        print('Cleaning resources ...')
        self.log.debug('Cleaning resources ...')
        self.console.stop()
        self.requester.close()
        self.subscriber.close()
        self.console.join(timeout=0.1)

    def stop(self):
        print("Stopping ...")
        self.active = False
        self.log.debug('done *')
