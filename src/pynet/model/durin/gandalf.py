from . import Exit, Execute, URL_REQUEST_CLIENT, URL_CONSOLE_CLIENT
from .. import Node
from threading import Thread


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


class Gandalf(Node):
    requester: Node.Requester
    console: Console

    def __init__(self):
        Node.__init__(self, 'DurinServer', enable_signal=True)
        self.requester = self.new_requester(URL_REQUEST_CLIENT)
        self.console = Console(self)
        self.console.start()
        self.log.debug('done *')

    def demand(self, cmd: str):
        self.requester.send(Execute(command=cmd))
        res = self.requester.receive()
        self.log.debug(f'{self} done {res}')

    def clean_resources(self):
        self.console.stop()
        # self.requester.send(Exit())
