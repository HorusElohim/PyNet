from typing import Any
import subprocess
from threading import Thread
from .. import Node, Url, Process
from . import Execute, URLS


class ConsoleExecutor(Thread):
    publisher: Node.Publisher
    active: bool = False

    def __init__(self, publisher: Node.Publisher, cmd: str):
        Thread.__init__(self)
        self.publisher = publisher
        self.cmd = cmd

    def run(self) -> None:
        self.active = True
        proc = subprocess.Popen([self.cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while self.active:
            out = proc.stdout.read()
            err = proc.stdout.read()
            self.publisher.send(out.decode().strip())
            self.publisher.send(err.decode().strip())
            if proc.wait(timeout=0.1) == 0:
                self.active = False
        proc.terminate()

    def stop(self):
        self.active = False


class DurinDoor(Node):
    replier: Node.Replier
    publisher: Node.Publisher
    executor: ConsoleExecutor
    active: bool = False

    def __init__(self):
        Node.__init__(self, 'DurinServer', enable_signal=True)
        self.replier = self.new_replier(URLS.server.demander)
        self.publisher = self.new_publisher(URLS.server.console)
        self.executor = None
        self.log.debug('done *')

    def start(self):
        print('Durin Door has started!')
        self.active = True
        while self.active:
            req = self.replier.receive()
            if self.executor and self.executor.active:
                self.executor.stop()
                self.executor.join()
            rep = self.dispatch(req)
            if rep == 'exit':
                return
            self.replier.send(rep)
        print('[x] Closed')
        self.log.debug('done * ')

    def dispatch(self, data: Any) -> Any:
        self.log.debug(f' <- {data}')
        response = False
        if isinstance(data, Execute):
            if data.command == 'exit':
                self.active = False
                self.clean_resources()
                print('[x] Exit')
                return 'exit'
            else:
                print(f'[-] > {data.command}')
                try:
                    self.executor = ConsoleExecutor(self.publisher, data.command)
                    self.executor.start()
                    response = True
                except Exception as ex:
                    response = False
                    self.log.error(f'Error starting ConsoleExecutor - Exception: {ex}')
        self.log.debug(f' -> {response}')
        return response

    def console_output(self, line: str):
        self.publisher.send(line)

    def clean_resources(self):
        self.replier.close()
        self.publisher.close()
