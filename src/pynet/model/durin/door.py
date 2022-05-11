from typing import Any
import subprocess
from threading import Thread
from .. import Node, Url, Process
from . import Execute, URLS

from subprocess import Popen, PIPE
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read, system


class ConsoleExecutor(Thread):
    publisher: Node.Publisher
    active: bool = False

    def __init__(self, publisher: Node.Publisher, cmd: str):
        Thread.__init__(self)
        self.publisher = publisher
        self.cmd = cmd

    def run(self) -> None:
        self.active = True
        # run the shell as a subprocess:
        p = Popen([self.cmd], stdout=PIPE)
        # set the O_NONBLOCK flag of p.stdout file descriptor:
        flags = fcntl(p.stdout, F_GETFL)  # get current p.stdout flags
        fcntl(p.stdout, F_SETFL, flags | O_NONBLOCK)

        # while self.active:
        while True:
            try:
                result = read(p.stdout.fileno(), 1024).decode("utf-8")
                self.publisher.send(result.strip())
            except OSError:
                # the os throws an exception if there is no data
                sleep(0.1)
                continue

        fcntl(p.stdout, F_SETFL, flags)
        p.terminate()

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
            self.replier.send(rep)
            if rep == 'Closed':
                self.clean_resources()
        print('[x] Closed')
        self.log.debug('done * ')

    def dispatch(self, data: Any) -> Any:
        self.log.debug(f' <- {data}')
        response = False
        if isinstance(data, Execute):
            if data.command == 'close':
                self.active = False
                print('[x] Closing')
                return 'Closed'
            elif data.command == 'CRTL-C':
                print(f'[CX] > {data.command}')
                if self.executor.active:
                    self.executor.stop()
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
